The code I used to drive my self-playing slide whistle [here](https://www.youtube.com/watch?v=7QtX_-pualw).

The Pure Data takes a midi file and compares the pitch on the microphone to the pitch of the note. It then based on the difference tells the servos how fast and in which direction to drive.

I was using [Purr Data](https://www.purrdata.net/) for the pd. The servos where driven by a Tiny 2040 from Pimoroni which was controlled via a serial stream from my laptop.
