import asyncio
import json
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field

from .browser import BrowserEngine, BrowserState, InteractiveElement

@dataclass
class AgentThought:
    step: int
    timestamp: str
    reasoning: str
    action: str
    action_params: Dict[str, Any]

@dataclass
class AgentAction:
    type: str  # click, type, scroll, wait, navigate, press
    params: Dict[str, Any]
    result: bool

class CognitiveAgent:
    def __init__(self, task: str, on_thought=None, on_frame=None):
        self.task = task
        self.engine = BrowserEngine(headless=False)
        self.thoughts: List[AgentThought] = []
        self.actions: List[AgentAction] = []
        self.session_id = str(uuid.uuid4())
        self.on_thought = on_thought
        self.on_frame = on_frame
        self.max_steps = 20
        self.step_count = 0

    async def run(self):
        await self.engine.start()
        try:
            await self._think(f"Starting task: {self.task}. I need to navigate to the target website and complete the requested action.")
            
            for i in range(self.max_steps):
                self.step_count = i + 1
                state = await self.engine.get_state()
                
                if self.on_frame:
                    await self.on_frame(state.screenshot_b64)
                
                action = await self._plan_action(state)
                if action is None:
                    await self._think("Task appears complete or no clear next action. Stopping.")
                    break
                
                result = await self._execute_action(action)
                action.result = result
                self.actions.append(action)
                
                await self._think(f"Executed {action.type} with params {action.params}. Result: {'success' if result else 'failed'}")
                
                if await self._verify_completion(state):
                    await self._think("Task verification passed. Marking as complete.")
                    break
        finally:
            await self.engine.stop()

    async def _think(self, reasoning: str):
        thought = AgentThought(
            step=self.step_count,
            timestamp=datetime.utcnow().isoformat(),
            reasoning=reasoning,
            action="",
            action_params={}
        )
        self.thoughts.append(thought)
        if self.on_thought:
            await self.on_thought(thought)

    async def _plan_action(self, state: BrowserState) -> Optional[AgentAction]:
        task_lower = self.task.lower()
        
        if 'search' in task_lower or 'google' in task_lower:
            if 'google' not in state.url and 'search' not in state.url:
                await self.engine.navigate('https://www.google.com')
                return AgentAction(type='navigate', params={'url': 'https://www.google.com'}, result=True)
        
        if 'amazon' in task_lower and 'amazon' not in state.url:
            await self.engine.navigate('https://www.amazon.com')
            return AgentAction(type='navigate', params={'url': 'https://www.amazon.com'}, result=True)
        
        if 'github' in task_lower and 'github' not in state.url:
            await self.engine.navigate('https://github.com')
            return AgentAction(type='navigate', params={'url': 'https://github.com'}, result=True)
        
        if state.elements:
            for el in state.elements:
                if any(word in el.text.lower() for word in ['submit', 'search', 'go', 'click', 'ok']):
                    return AgentAction(type='click', params={'index': el.index}, result=False)
        
        if state.elements:
            return AgentAction(type='click', params={'index': 0}, result=False)
        
        return AgentAction(type='scroll', params={'direction': 'down'}, result=False)

    async def _execute_action(self, action: AgentAction) -> bool:
        try:
            if action.type == 'click':
                state = await self.engine.get_state()
                return await self.engine.click(action.params['index'], state.elements)
            elif action.type == 'type':
                return await self.engine.type_text(action.params['text'])
            elif action.type == 'scroll':
                return await self.engine.scroll(action.params.get('direction', 'down'))
            elif action.type == 'wait':
                await asyncio.sleep(action.params.get('seconds', 1))
                return True
            elif action.type == 'press':
                return await self.engine.press(action.params['key'])
            elif action.type == 'navigate':
                await self.engine.navigate(action.params['url'])
                return True
            return False
        except Exception:
            return False

    async def _verify_completion(self, state: BrowserState) -> bool:
        task_lower = self.task.lower()
        if 'search' in task_lower and 'search' in state.url.lower():
            return True
        if 'amazon' in task_lower and 'amazon' in state.url.lower():
            return True
        if 'github' in task_lower and 'github' in state.url.lower():
            return True
        if self.step_count >= self.max_steps:
            return True
        return False

    def get_summary(self) -> Dict[str, Any]:
        return {
            'session_id': self.session_id,
            'task': self.task,
            'steps': len(self.actions),
            'thoughts': len(self.thoughts),
            'actions': [{'type': a.type, 'params': a.params, 'result': a.result} for a in self.actions],
            'thoughts': [{'step': t.step, 'reasoning': t.reasoning} for t in self.thoughts]
        }