'''
Scrapes images and other data  of current MPs in the cabinet
from the url http://164.100.47.132/LssNew/Members/Statewiselist.aspx

uses the foll libraries
requests
BeautifulSoup
PIL(Wand)
StringIO
'''
import base64

__author__ = 'Pranav Tendolkar'

import  requests
from bs4 import BeautifulSoup
import re
from PIL import Image, ImageChops
import io
#python 2.x
#import cStringIO


states = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
          'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
          'Meghalaya', 'Mizoram', 'Nagaland','Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
          'Uttarakhand', 'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
          'Lakshadweep', 'Puducherry']
stateurl='http://164.100.47.132/LssNew/Members/statedetail.aspx'
imageurl='http://164.100.47.132/mpimage/photo/'

def query():


    for state in states:
        param={'state_code':state}
        session=requests.session()
        r=session.get(stateurl,params=param)
        response=BeautifulSoup(r.text)
        links=response.find(id='ctl00_ContPlaceHolderMain_Statedetail1_dg1').find_all('a')
        for link in links:
            url='http://164.100.47.132/LssNew/Members/'+link.get('href')
            code=re.search('[0-9]*$',link.get('href')).group()
            image=getimage(code)


            ##write code to associate with MP


            print(code)
            resp=BeautifulSoup(requests.get(url).text)
            # print(resp)
            member={}
            break

        break



def getimage(code):
    full_imageurl=imageurl+code+'.jpg'
    r=requests.get(full_imageurl)

    if r.status_code ==200:
        r.raw.decode_content = True
        with open('test.jpg', 'wb') as f:
            f.write(r.content)

        stream = io.BytesIO(r.content)
        im=Image.open(stream)
        im=trim(im)

        #Python 2.7 code
        # jpeg_image_buffer = cStringIO.StringIO()

        jpeg_image_buffer = io.BytesIO()
        im.save(jpeg_image_buffer, format="JPEG")
        imgStr = base64.b64encode(jpeg_image_buffer.getvalue())

        #Testing
        # fh = open("decoded.jpg", "wb")
        # fh.write(base64.decodestring(imgStr))
        # fh.close()
        return imgStr
        im.save('cropped.jpg')

    else:
        raise Exception('Errr getting image')


#remove white box from the image
def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)



query()