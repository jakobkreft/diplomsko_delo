# Diplomsko delo: Vgrajena zasebnost pri videonadzoru prometa

- Avtor: Jakob Kreft
- Mentor: izr. prof. dr. Janez Perš, univ. dipl. inž. el.
- Somentorica: as. Marija Ivanovska, mag. inž. el.
- Ljubljana, 2023
- Univerza v Ljubljani

### koda/
1. `trigger_Server.py`: sproži snemanje na obeh kamerah.
2. `rvid.py`: koda na Raspberry pi za snemaje ob sprožitvi.


1. `sequencer.py`: Video pretvori v zaporedje slik.
2. `align.py`: Slike leve in desne kamere se ujemajo.
3. `cropper.py`: Slikam odstranimo črne robove.
4. `detr.py`: Zazna in shrani robne okvirje objektov.
5. `CsvtoSingleCOCOvehicle.py`: Iz CSV dobimo posamezne JSON.
6. `imgviewer.py`: Ročno pregledamo in popravimo napake.
7. `jsonstoCOCOjson.py`: JSON prevedemo v format COCO.

### faze snemanja
<img width="280" alt="faze3" src="https://github.com/jakobkreft/diplomsko_delo/assets/70409100/1edcebc0-ddd4-4ca0-9c36-8bebb41787c9">

### sinhrono snemanje
<img width="320" alt="triggerinrvid" src="https://github.com/jakobkreft/diplomsko_delo/assets/70409100/69c892e3-a2ae-49f1-97e1-989cb821fb66">

### postopek obdelave do končne baze slik
<img width="220" alt="pipeline" src="https://github.com/jakobkreft/diplomsko_delo/assets/70409100/fedbc3d2-ae01-4c86-96ca-77d1e1b76f80">
