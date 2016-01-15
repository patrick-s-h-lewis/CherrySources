import sys
import json
import os
import pickle
import json
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
import SeekSpider
import CherryPipelines
    
def finalise_file(file):
    with open(file,'ab+') as f:
        f.write('{}]')

index = int(sys.argv[1])
subdir = 'data'

with open('uk depts.json','r') as f:
    j = json.load(f)
    subdir = subdir+'/'+j[index]['name']
    outfile= subdir+ '/'+'urls.json'
    scrapy_stats=subdir + '/'+'stats.json'
    s_u = [j[index]['url']]
    a_d = [j[index]['root'].split('/')[0]]
    intermediate = j[index]['root'].split('/')[1:]
    if len(intermediate)>0:
        root = '\/'+'\/'.join(intermediate)+'\/.*'
    else: 
        root = '.*'
    print('')
    print(s_u)
    print(j[index]['root'])
    print(a_d)
    print(root)
os.mkdir(subdir)  
with open(outfile,'wb+') as f:
    f.write('[')

with open(scrapy_stats,'wb+') as f:
    f.write('')

settings = Settings()
settings.set('ITEM_PIPELINES', {
    'CherryPipelines.SeekPipeline': 100
})
settings.set('RETRY_ENABLED',True)
settings.set('RETRY_TIMES',3)

#settings.set('LOG_ENABLED',True)
settings.set('FILE_NAME',outfile)
settings.set('SCRAPY_FILE_NAME',scrapy_stats)
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

runner = CrawlerRunner(settings)
runner.crawl(
    SeekSpider.SeekSpider,
    s_u=s_u,
    a_d=a_d,
    root=root
    )
d=runner.join()
d2 = d.addBoth(lambda _:reactor.stop())
d2.addCallback(lambda _:finalise_file(outfile))
reactor.run()
