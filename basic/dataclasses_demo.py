from dataclasses import dataclass

from dataclasses import astuple, dataclass, fields


@dataclass
class ImgInfo:
    image: dict = None
    file_path: str = None
    result: str = None


@dataclass
class ImgLog:
    raw: ImgInfo = None
    paticle: ImgInfo = None

    def __iter__(self):
        yield from astuple(self)


# for attr, value in a.__dict__.iteritems():
#    print attr, value
a = ImgLog(ImgInfo(), ImgInfo())
# a.raw.image = 1
a.paticle.result = 1

barcode_no = 'barcode'

for k, v in a.__dict__.items():
    # a.__dict__[k].
    file_name = '[{}][{}][{}].jpg'.format(k,v, barcode_no)
