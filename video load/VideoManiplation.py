import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QInputDialog

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        # Create a timer for updating video frames and set its timeout slot
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrame)
        # Create a media player for video and audio playback
        self.mediaPlayer = QMediaPlayer()
        # Create a label for displaying video frames
        self.label = QLabel()
        # Create a label for displaying the current time
        self.timeLabel = QLabel()
        self.timeLabel.setAlignment(Qt.AlignCenter)
        # Create play, stop, load, and speed buttons
        self.playButton = QPushButton('Play')
        self.playButton.clicked.connect(self.play)
        self.stopButton = QPushButton('Stop')
        self.stopButton.clicked.connect(self.stop)
        self.loadButton = QPushButton('Load')
        self.loadButton.clicked.connect(self.load)
        self.speed1xButton = QPushButton('1x')
        self.speed1xButton.clicked.connect(self.play1x)
        self.speed2xButton = QPushButton('2x')
        self.speed2xButton.clicked.connect(self.play2x)
        self.speed3xButton = QPushButton('3x')
        self.speed3xButton.clicked.connect(self.play3x)
        # Create color filter buttons
        self.greenButton = QPushButton('Green')
        self.greenButton.clicked.connect(self.playGreen)
        self.blackButton = QPushButton('Black')
        self.blackButton.clicked.connect(self.playBlack)
        self.blueButton = QPushButton('Blue')
        self.blueButton.clicked.connect(self.playBlue) 
        self.nonecolorButton = QPushButton('Normal')
        self.nonecolorButton.clicked.connect(self.playNormal)

        # Create a layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.playButton)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.loadButton)
        layout.addWidget(self.speed1xButton)
        layout.addWidget(self.speed2xButton)
        layout.addWidget(self.speed3xButton)
        layout.addWidget(self.greenButton)
        layout.addWidget(self.blackButton)
        layout.addWidget(self.blueButton)
        layout.addWidget(self.nonecolorButton)
        layout.addWidget(self.timeLabel)  # Add time label to the layout
        self.setLayout(layout)

        # Variable to keep track of the current frame number
        self.frame_number = 0
        self.color_filter = None
  
    def playNormal(self):
        self.color_filter = None
        self.play() 

    def playGreen(self):
        self.color_filter = 'green'
        self.play()

    def playBlack(self):
        self.color_filter = 'black'
        self.play()

    def playBlue(self):
        self.color_filter = 'blue'
        self.play()

    def play1x(self):
        self.timer.start(round(1000. / 24))  # 24 frames per second

    def play2x(self):
        self.timer.start(round(1000. / 200))  # 12 frames per second

    def play3x(self):
        self.timer.start(round(1000. / 250))

    def load(self):
        choice, ok = QInputDialog.getItem(self, "Load Video", "Choose a source:", ["File", "Camera"], 0, False)
        if ok and choice == "File":
            fileName, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.avi *.mp4 *.flv *.mkv)")
            if fileName != '':
                self.cap = cv2.VideoCapture(fileName)  # Load the video file using OpenCV VideoCapture
                if not self.cap.isOpened():
                    print("Error opening video file")
                    return
                print("Video file loaded successfully")
                # Load the video file into the media player
                media_content = QMediaContent(QUrl.fromLocalFile(fileName))
                if media_content.isNull():
                    print("Failed to load media content")
                    return
                self.mediaPlayer.setMedia(media_content)
                print("Media content loaded successfully")
        elif ok and choice == "Camera":
            cameraNumber, ok = QInputDialog.getInt(self, "Camera Number", "Enter the camera number:", 0, 0, 10)
            if ok:
                self.cap = cv2.VideoCapture(cameraNumber)  # Capture video from the camera using OpenCV VideoCapture
                if not self.cap.isOpened():
                    print("Error opening camera")
                    return
                print("Camera opened successfully")


    def play(self):
        self.timer.start(round(1000. / 24))  # 24 frames per second
        self.mediaPlayer.play()

    def stop(self):
        self.timer.stop()
        self.mediaPlayer.stop()

    def nextFrame(self):
        ret, frame = self.cap.read()
        # Apply color filter
        if self.color_filter == 'GREEN':
            frame = frame * [0, 1, 0]  # Keep only green channel BGR -> 010 
        elif self.color_filter == 'RED':
            frame = frame * [0, 0, 1] # Keep only blue channel BGR -> 001
        elif self.color_filter == 'BLUE':
            frame = frame * [1, 0, 0]  # Keep only blue channel BGR -> 100
        frame = cv2.convertScaleAbs(frame) # Convert back to uint8
        # Skip frames based on playback speed
        if self.timer.isActive() and ret:
            self.frame_number += 1
            if self.frame_number % 2 == 0:  # Skip frames for 2x speed
                return
            if self.frame_number % 3 == 0:  # Skip frames for 3x speed
                return
        # Display the frame
        if ret:
            height, width, channel = frame.shape
            bytesPerLine = 3 * width  # assuming 3 channels (RGB)
            # Convert BGR to RGB because PyQt uses RGB to show the image and cv2 uses BGR
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Create QImage from RGB frame data because QLabel can display QImage but not numpy array
            img = QImage(rgbFrame.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pix = QPixmap.fromImage(img)  # Convert QImage to QPixmap
            self.label.setPixmap(pix)
            # Update the time label
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            current_time = self.frame_number / fps
            hours = int(current_time // 3600)
            minutes = int((current_time % 3600) // 60)
            seconds = int(current_time % 60)
            self.timeLabel.setText(f"Time: {hours:02d}:{minutes:02d}:{seconds:02d}")


# Create a window and set its properties 
if __name__ == "__main__":
    app = QApplication([])  # Create application
    player = VideoPlayer()
    player.show()
    app.exec_()
