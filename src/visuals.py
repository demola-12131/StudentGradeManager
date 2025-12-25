import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns

class AnalyticsCanvas(FigureCanvas):
    """
    Interactive visualization canvas for the GUI.
    Displays grade distributions and performance trends.
    """
    def __init__(self, parent=None):
        # Create two subplots: Bar chart and Line chart
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 4))
        self.fig.patch.set_facecolor('#1e293b') # Match Dark Theme
        super().__init__(self.fig)

    def update_charts(self, df):
        self.ax1.clear()
        self.ax2.clear()
        
        if not df.empty:
            # Set style for the charts
            sns.set_theme(style="dark")
            
            # Chart 1: Grade Frequency (Seaborn)
            order = ['A', 'B', 'C', 'D', 'E', 'F']
            sns.countplot(x='Grade', data=df, ax=self.ax1, hue='Grade', palette='viridis', order=order, legend=False)
            self.ax1.set_title("Grade Frequency Distribution", color='white')
            self.ax1.tick_params(colors='white')

            # Chart 2: Cumulative Performance Trend (Matplotlib)
            scores = df['Score'].tolist()
            self.ax2.plot(range(1, len(scores) + 1), scores, marker='o', color='#3b82f6')
            self.ax2.set_title("Performance Trend (Course by Course)", color='white')
            self.ax2.set_xlabel("Courses Added", color='white')
            self.ax2.set_ylabel("Score", color='white')
            self.ax2.tick_params(colors='white')

        self.fig.tight_layout()
        self.draw()