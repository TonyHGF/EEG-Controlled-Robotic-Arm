import pygame
import time
import math

# Initialize pygame
pygame.init()

# Set up the display
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)

# Define the font
font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

# Define the stimulus properties for each block
block_size = (100, 100)
# block_padding = 20  # Padding between blocks
row_padding = 20
col_padding = 80
num_cols = 3
num_rows = 4

# Define block properties (color, frequency, and phase)
block_properties = [
    {'color': (255, 255, 255), 'frequency': 9.25, 'phase': 0.0},    # Phase 0.0π
    {'color': (255, 255, 255), 'frequency': 11.25, 'phase': 0.0},   # Phase 0.0π
    {'color': (255, 255, 255), 'frequency': 13.25, 'phase': 0.0},   # Phase 0.0π
    {'color': (255, 255, 255), 'frequency': 9.75, 'phase': 0.5},    # Phase 0.5π
    {'color': (255, 255, 255), 'frequency': 11.75, 'phase': 0.5},   # Phase 0.5π
    {'color': (255, 255, 255), 'frequency': 13.75, 'phase': 0.5},   # Phase 0.5π
    {'color': (255, 255, 255), 'frequency': 10.25, 'phase': 1.0},   # Phase 1.0π
    {'color': (255, 255, 255), 'frequency': 12.25, 'phase': 1.0},   # Phase 1.0π
    {'color': (255, 255, 255), 'frequency': 14.25, 'phase': 1.0},   # Phase 1.0π
    {'color': (255, 255, 255), 'frequency': 10.75, 'phase': 1.5},   # Phase 1.5π
    {'color': (255, 255, 255), 'frequency': 12.75, 'phase': 1.5},   # Phase 1.5π
    {'color': (255, 255, 255), 'frequency': 14.75, 'phase': 1.5},   # Phase 1.5π
]

num_dir = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: '*', 10: '0', 11: '#'}

# Initialize blocks with positions
blocks = []
for i in range(num_rows):
    for j in range(num_cols):
        index = i * num_cols + j
        if index < len(block_properties):
            # x_pos = j * (block_size[0] + block_padding) + block_padding
            # y_pos = i * (block_size[1] + block_padding) + block_padding
            x_pos = j * (block_size[0] + col_padding) + col_padding
            y_pos = i * (block_size[1] + row_padding) + row_padding
            blocks.append({
                'color': block_properties[index]['color'],
                'size': block_size,
                'position': (x_pos, y_pos),
                'frequency': block_properties[index]['frequency'],
                'phase': block_properties[index]['phase']
            })

# Main loop
running = True
start_time = time.time()

while running:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear screen

    for i, block in enumerate(blocks):
        frequency = block['frequency']
        phase = block['phase']
        cycle_time = 1.0 / frequency
        t = (elapsed_time + phase * math.pi) % cycle_time  # Adjust time by phase
        brightness = 255 if t < cycle_time / 2 else 0  # Simple on-off blinking
        block_color = (brightness, brightness, brightness)

        pygame.draw.rect(screen, block_color, (*block['position'], *block['size']))
         # Draw the frequency text in the center of the block
        frequency_text = font.render(num_dir[i], True, (0, 0, 0))
        # frequency_text = font.render(f"{block['frequency']} Hz", True, (0, 0, 0))
        text_rect = frequency_text.get_rect(center=(block['position'][0] + block_size[0] // 2, block['position'][1] + block_size[1] // 2))
        screen.blit(frequency_text, text_rect)

        

    pygame.display.flip()  # Update the full display Surface to the screen

    pygame.time.delay(50)  # Delay to limit the update rate

pygame.quit()