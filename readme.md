# Motion Extraction as per Posy

This is a quick implementation of video motion extraction, using the method
proposed by [Posy](https://www.youtube.com/@PosyMusic) in his video on Motion
Extraction. (Yes, that splotchy image below is a video link, click it to watch
Posy's inspiring video).

[![Motion Extraction](https://img.youtube.com/vi/NSS6yAMZF78/hqdefault.jpg)](https://www.youtube.com/embed/NSS6yAMZF78)

It was actually [Steve Mould](https://www.youtube.com/@SteveMould) who got me
interested in video motion amplification. but I never got round to anything like
experimental implementation. The math behind
[Eulerian Video Magnification](https://people.csail.mit.edu/mrub/evm/) was
always a bit daunting. When I ran into Posy's video, making this proof of
concept was quick and easy.

[![Reveal Invisible Motion With This Clever Video Trick](https://img.youtube.com/vi/rEoc0YoALt0/hqdefault.jpg)](https://www.youtube.com/embed/rEoc0YoALt0)

Just to be clear: the code in this repository does _not_ implement Eulerian,
only the simplified version that Posy proposes.

Hope this helps.

## Running

```sh
$ pip3 install python-opencv numpy
$ python3 posy-motion-extraction.py some-video.mp4
```

