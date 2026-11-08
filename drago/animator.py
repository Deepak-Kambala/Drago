"""
Animation controller and state sequencing for Drago.
Handles idle looping, roar action bursts, and evolution metamorphosis sequences.
"""

import math
from typing import List, Optional
import copy
from PIL import Image
from drago.config import DragoConfig
from drago.evolution import DragonState
from drago.renderer import DragonRenderer

class DragonAnimator:
    def __init__(self, config: DragoConfig, state: DragonState):
        self.config = config
        self.state = state
        self.renderer = DragonRenderer(config, state)

    def generate_idle(self) -> List[Image.Image]:
        """
        Generates the standard README idle animation:
        - Breathing
        - Periodic eye blink
        - Tail organic wave
        - Wing subtle rise and fold
        - Head and eye tracking
        """
        return self.renderer.render_animation(action="idle")

    def generate_roar(self) -> List[Image.Image]:
        """
        Generates rare special action animation:
        Dragon raises head, opens maw showing teeth, flares wings,
        chest expands, and settles back into idle posture.
        """
        return self.renderer.render_animation(action="roar")

    def generate_evolution(self, previous_state: DragonState, next_state: DragonState, transition_frames: int = 36) -> List[Image.Image]:
        """
        Generates dynamic metamorphosis sequence:
        Existing dragon -> body expands -> horns develop -> spikes appear ->
        wings enlarge -> armor locks on -> energy surge -> new evolved form!
        Communicates actual physical growth, not a static image switch.
        """
        frames = []
        for i in range(transition_frames):
            t = i / max(1, transition_frames - 1)  # 0.0 to 1.0

            # Interpolate anatomical properties smoothly using smoothstep
            # s = t * t * (3 - 2 * t)
            s = t * t * (3.0 - 2.0 * t)

            # Phased unlocks:
            # 0.0 - 0.35: body expands and aura begins to spark
            # 0.20 - 0.60: horns and tail blade lengthen
            # 0.40 - 0.80: dorsal spikes erupt along spine
            # 0.50 - 0.90: wings expand outwards
            # 0.70 - 1.00: armor plates lock into place

            interp_state = copy.deepcopy(next_state)
            interp_state.body_scale = previous_state.body_scale + (next_state.body_scale - previous_state.body_scale) * s
            interp_state.wing_span_multiplier = previous_state.wing_span_multiplier + (next_state.wing_span_multiplier - previous_state.wing_span_multiplier) * s
            interp_state.tail_length_multiplier = previous_state.tail_length_multiplier + (next_state.tail_length_multiplier - previous_state.tail_length_multiplier) * s
            interp_state.horn_curvature = previous_state.horn_curvature + (next_state.horn_curvature - previous_state.horn_curvature) * s

            # Energy aura surges during transformation
            surge = math.sin(t * math.pi) * 0.7
            interp_state.aura_intensity = min(1.0, previous_state.aura_intensity + surge)

            # Discrete features switch at thresholds
            interp_state.horn_level = previous_state.horn_level if t < 0.35 else next_state.horn_level
            interp_state.dorsal_spike_count = previous_state.dorsal_spike_count if t < 0.50 else next_state.dorsal_spike_count
            interp_state.wing_level = previous_state.wing_level if t < 0.65 else next_state.wing_level
            interp_state.armor_level = previous_state.armor_level if t < 0.80 else next_state.armor_level
            interp_state.tail_level = previous_state.tail_level if t < 0.45 else next_state.tail_level

            # Render frame with roaring energy at the peak of evolution
            action = "roar" if 0.4 <= t <= 0.75 else "idle"
            frame = self.renderer.render_frame(
                frame_idx=i % self.config.frame_count,
                total_frames=self.config.frame_count,
                action=action,
                state_override=interp_state,
            )
            frames.append(frame)

        return frames
