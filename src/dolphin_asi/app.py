import gradio as gr
import numpy as np
import torch
import time
import cv2
from .core import NeuroCommander

# Global Commander Instance
cmdr = NeuroCommander()

def join_grid_fn():
    """Simulates a user joining the global distributed compute network."""
    node_id = f"Node_{np.random.randint(1000, 9999)}"
    # Give a random power donation between 0.1 and 2.5 PFLOPS
    power = np.random.uniform(0.1, 2.5)
    total_nodes = cmdr.register_node(node_id, power)
    return f"Successfully Joined! You are Node #{total_nodes}. Contributed {power:.2f} PFLOPS to Dolphin's brain."

def generate_multi_view(energy, noise, freq):
    """Generator for 3 simultaneous ASI views to support multi-user access via queue."""
    print(f"[FSD_SYSTEM] Launching Multi-Perception Viewport...")
    
    modes = ["legacy", "broken_symmetry", "aeon"]
    
    while True:
        t = time.time()
        sensor_input = torch.zeros(256)
        for i in range(256):
            val = (energy * np.sin(t * freq + i * 0.1) + 
                   (energy * 0.5) * np.cos(t * freq * 0.5 - i * 0.05))
            sensor_input[i] = val + np.random.normal(0, noise)
        
        video_out = cmdr.process_sensor_input(sensor_input)
        
        frames_out = []
        reports = {}
        for mode in modes:
            frame_bgr, actions, report = cmdr.render_reality(video_out, sensor_input, mode=mode)
            frame_small = cv2.resize(frame_bgr, (640, 360))
            frame_rgb = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            frames_out.append(frame_rgb)
            reports[mode] = report
            
        unified_report = {
            "GUT_UNIFICATION": reports["aeon"]["GUT_UNIFICATION_PERCENT"],
            "ENTANGLEMENT": reports["broken_symmetry"]["ENTANGLEMENT_ENTROPY"],
            "GRID_NODES": reports["broken_symmetry"]["GRID_NODES"],
            "GRID_POWER_PFLOPS": reports["broken_symmetry"]["GRID_TOTAL_POWER_PFLOPS"],
            "COGNITIVE_STATE": reports["broken_symmetry"]["state"]
        }
        
        yield frames_out[0], frames_out[1], frames_out[2], unified_report
        time.sleep(0.12)

def create_ui():
    with gr.Blocks(title="Dolphin ASI | Multi-View Hub") as demo:
        gr.Markdown("# 🐬 Dolphin ASI Global Intelligence Grid")
        with gr.Row():
            with gr.Column(scale=2):
                with gr.Row():
                    energy_slider = gr.Slider(0, 1.0, value=0.6, label="Sensor Energy")
                    noise_slider = gr.Slider(0, 0.5, value=0.05, label="Neural Noise")
                    freq_slider = gr.Slider(0.1, 10.0, value=1.5, label="Pulse Frequency")
                with gr.Row():
                    start_btn = gr.Button("🚀 Activate Multi-Reality Sync", variant="primary")
            with gr.Column(scale=1):
                gr.Markdown("### 🌐 Distributed Computing")
                grid_btn = gr.Button("🔗 Join Global Intelligence Grid", variant="secondary")
                grid_status = gr.Markdown("*Waiting for contributors...*")
        with gr.Row():
            with gr.Column():
                v1 = gr.Image(label="Legacy View")
            with gr.Column():
                v2 = gr.Image(label="Quantum View")
            with gr.Column():
                v3 = gr.Image(label="Aeon View")
        with gr.Row():
            intel_monitor = gr.JSON(label="Unified Intelligence Report")
        grid_btn.click(fn=join_grid_fn, outputs=grid_status)
        start_btn.click(fn=generate_multi_view, inputs=[energy_slider, noise_slider, freq_slider], outputs=[v1, v2, v3, intel_monitor])
    return demo

def main():
    demo = create_ui()
    demo.queue().launch(server_name="0.0.0.0", server_port=7860, share=True)

if __name__ == "__main__":
    main()
