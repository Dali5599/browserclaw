import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("browserclaw.vision")

try:
    import torch
    from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
    from qwen_vl_utils import process_vision_info
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class VisionLLMService:
    def __init__(self, model_id: str = "Qwen/Qwen2.5-VL-7B-Instruct", device: str = "cuda" if (TRANSFORMERS_AVAILABLE and torch.cuda.is_available()) else "cpu"):
        self.model_id = model_id
        self.device = device
        self.model = None
        self.processor = None
        self.loaded = False

    def load_model(self):
        if not TRANSFORMERS_AVAILABLE:
            logger.error("Transformers or qwen-vl-utils not installed. Vision LLM cannot be loaded.")
            return False
        
        if self.loaded:
            return True

        try:
            logger.info(f"Loading Vision-LLM model {self.model_id} on {self.device}...")
            self.model = Qwen2VLForConditionalGeneration.from_pretrained(
                self.model_id,
                torch_dtype=torch.bfloat16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            if self.device == "cpu":
                self.model.to(self.device)
            
            self.processor = AutoProcessor.from_pretrained(self.model_id)
            self.loaded = True
            logger.info("Vision-LLM model loaded successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to load Vision-LLM model: {e}")
            return False

    def detect_bounding_box(self, image_path: str, prompt: str) -> List[Dict[str, Any]]:
        """
        Detects bounding boxes for a given prompt in an image using Qwen2.5-VL.
        Returns a list of dicts with label, box_2d ([ymin, xmin, ymax, xmax] normalized 0-1000).
        """
        if not self.loaded and not self.load_model():
            logger.warning("Vision model is not loaded. Returning empty detections.")
            return []

        try:
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_path},
                        {"type": "text", "text": f"{prompt}. Output format: [ymin, xmin, ymax, xmax] normalized to 1000."},
                    ],
                }
            ]

            text = self.processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            image_inputs, video_inputs = process_vision_info(messages)
            inputs = self.processor(
                text=[text],
                images=image_inputs,
                videos=video_inputs,
                padding=True,
                return_tensors="pt"
            )
            inputs = inputs.to(self.device)

            generated_ids = self.model.generate(**inputs, max_new_tokens=128)
            generated_ids_trimmed = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
            ]
            output_text = self.processor.batch_decode(
                generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )[0]

            logger.info(f"Vision LLM output: {output_text}")
            
            # Simple parsing of box coordinates if generated in bracket format e.g. [ymin, xmin, ymax, xmax]
            import re
            boxes = []
            matches = re.findall(r'\[([0-9,\s]+)\s*\]', output_text)
            for match in matches:
                try:
                    parts = [int(p.strip()) for p in match.split(',')]
                    if len(parts) == 4:
                        boxes.append({
                            "box_2d": parts,
                            "label": prompt,
                            "raw": output_text
                        })
                except Exception:
                    continue

            return boxes
        except Exception as e:
            logger.error(f"Error during vision detection: {e}")
            return []

vision_service = VisionLLMService()
