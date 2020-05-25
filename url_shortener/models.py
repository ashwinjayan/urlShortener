import random, string, hashlib
from random import choices
from .extension import db
from datetime import datetime

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), unique=True)
    short_url = db.Column(db.String(8), unique=True)
    visits = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()

    
    def generate_short_link(self):
        #characters = string.digits + string.ascii_letters
        #short_url = ''.join(choices(characters, k=3))
        #num = random.randint(0, 10000)
        short_url = self.encode(self.original_url)

        link = self.query.filter_by(short_url=short_url).first()
        if link:
            return self.generate_short_link()

        return short_url

    def encode(self, longUrl):
        """ Encodes a URL to a shortened URL
        :type longUrl str
        :rtype: str
        """
        md5_hash = hashlib.md5(longUrl.encode('utf-8')).hexdigest()
        #md5_has has 32 bytes
        # get 3 slices of 10 bytes each and xor them so we end up with shorter URL suffix of len 8
        size = len(md5_hash)
        threeQ = int(size/3)

        x = md5_hash[:threeQ]
        y = md5_hash[threeQ:-threeQ]
        z = md5_hash[-threeQ:]

        xored = int(x, 16) ^ int(y, 16) ^ int(z, 16)

        return self.base62_encode(xored)

    def base62_encode(self, num):
        alphabet = string.digits + string.ascii_letters
        """Encode a positive number in Base X

        Arguments:
        - `num`: The number to encode
        """
        hash_str = []
        while num:
            num, r = divmod(num, len(alphabet))
            hash_str.append(alphabet[r])
        return ''.join(hash_str)