import pygame
import numpy as np
import time
from src.maze import create_maze
from src.explorer import Explorer
from src.constants import CELL_SIZE, WINDOW_SIZE, BLUE, WHITE

def visualize_optimal_paths():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE * 2, WINDOW_SIZE))  # Double width for side by side
    pygame.display.set_caption("Explorer Comparison: Enhanced vs Original")
    clock = pygame.time.Clock()

    # Create maze and explorers
    maze = create_maze(50, 50, "static")  # Use create_maze function
    enhanced_explorer = Explorer(maze, visualize=True)  # Enhanced explorer with visualization
    original_explorer = Explorer(maze, visualize=True)  # Original explorer with visualization
    
    # Get optimal paths using both explorers
    enhanced_start_time = time.time()
    enhanced_path = enhanced_explorer.a_star_search(heuristic_type="euclidean")
    enhanced_end_time = time.time()
    enhanced_time_taken = enhanced_end_time - enhanced_start_time
    
    original_start_time = time.time()
    original_path = original_explorer.a_star_search(heuristic_type="euclidean")
    original_end_time = time.time()
    original_time_taken = original_end_time - original_start_time
    
    # Colors
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    ENHANCED_COLOR = (64, 224, 208)  # Turquoise
    ORIGINAL_COLOR = (255, 165, 0)   # Orange
    
    def draw_maze(offset_x, path_so_far, current_pos, path_color, title):
        # Draw maze
        for y in range(maze.height):
            for x in range(maze.width):
                if maze.grid[y][x] == 1:
                    pygame.draw.rect(screen, BLACK,
                                   (offset_x + x * CELL_SIZE, y * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE))
        
        # Draw path so far
        for pos in path_so_far:
            pygame.draw.rect(screen, path_color,
                           (offset_x + pos[0] * CELL_SIZE, pos[1] * CELL_SIZE,
                            CELL_SIZE, CELL_SIZE))
        
        # Draw start and end points
        pygame.draw.rect(screen, GREEN,
                        (offset_x + maze.start_pos[0] * CELL_SIZE,
                         maze.start_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED,
                        (offset_x + maze.end_pos[0] * CELL_SIZE,
                         maze.end_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Draw current position
        pygame.draw.rect(screen, YELLOW,
                        (offset_x + current_pos[0] * CELL_SIZE,
                         current_pos[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))
        
        # Draw title
        font = pygame.font.Font(None, 36)
        text = font.render(title, True, BLACK)
        screen.blit(text, (offset_x + 10, 10))
        
        # Draw step counter
        steps_text = font.render(f'Steps: {len(path_so_far)}', True, BLACK)
        screen.blit(steps_text, (offset_x + 10, 40))

    def draw_state(enhanced_path_so_far, original_path_so_far, enhanced_pos, original_pos):
        screen.fill(WHITE)
        
        # Draw Enhanced explorer path
        draw_maze(0, enhanced_path_so_far, enhanced_pos, ENHANCED_COLOR, "Enhanced Explorer")
        
        # Draw Original explorer path
        draw_maze(WINDOW_SIZE, original_path_so_far, original_pos, ORIGINAL_COLOR, "Original Explorer")
        
        # Draw legend at the top of the screen
        legend_x = WINDOW_SIZE - 150  # Position legend near the middle
        legend_y = 10  # Position at the top
        legend_items = [
            ("Start", GREEN),
            ("End", RED),
            ("Current", YELLOW),
            ("Enhanced", ENHANCED_COLOR),
            ("Original", ORIGINAL_COLOR)
        ]
        
        # Draw legend background
        pygame.draw.rect(screen, WHITE, (legend_x - 5, legend_y - 5, 160, 130))
        pygame.draw.rect(screen, BLACK, (legend_x - 5, legend_y - 5, 160, 130), 1)
        
        font = pygame.font.Font(None, 24)
        for i, (item, color) in enumerate(legend_items):
            pygame.draw.rect(screen, color, (legend_x, legend_y + i*25, 20, 20))
            text = font.render(item, True, BLACK)
            screen.blit(text, (legend_x + 25, legend_y + i*25 + 2))
        
        pygame.display.flip()
        clock.tick(30)  # Control visualization speed

    # Main visualization loop
    enhanced_path_so_far = []
    original_path_so_far = []
    enhanced_pos = maze.start_pos
    original_pos = maze.start_pos
    
    running = True
    enhanced_idx = 0
    original_idx = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update paths
        if enhanced_idx < len(enhanced_path):
            enhanced_pos = enhanced_path[enhanced_idx]
            enhanced_path_so_far.append(enhanced_pos)
            enhanced_idx += 1
            
        if original_idx < len(original_path):
            original_pos = original_path[original_idx]
            original_path_so_far.append(original_pos)
            original_idx += 1
            
        # Draw current state
        draw_state(enhanced_path_so_far, original_path_so_far, enhanced_pos, original_pos)
        
        # Check if both paths are complete
        if enhanced_idx >= len(enhanced_path) and original_idx >= len(original_path):
            # Print performance comparison
            print("\n=== Performance Comparison ===")
            print(f"Enhanced Explorer:")
            print(f"Total time taken: {enhanced_time_taken:.4f} seconds")
            print(f"Total moves made: {len(enhanced_path)}")
            print(f"Average moves per second: {len(enhanced_path)/enhanced_time_taken:.2f}")
            
            print(f"\nOriginal Explorer:")
            print(f"Total time taken: {original_time_taken:.4f} seconds")
            print(f"Total moves made: {len(original_path)}")
            print(f"Average moves per second: {len(original_path)/original_time_taken:.2f}")
            print("=============================\n")
            
            # Save final state
            pygame.image.save(screen, "explorer_comparison.png")
            pygame.time.wait(2000)  # Wait 2 seconds before closing
            running = False
    
    pygame.quit()

if __name__ == "__main__":
    visualize_optimal_paths() 