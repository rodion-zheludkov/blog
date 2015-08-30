import itertools

def split_seq(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))


def write_header(fw, tag):
    fw.write('---\n')
    fw.write('layout: wedding\n')
    fw.write('wedding_tag: %s\n' % tag)
    fw.write('---\n')

def write_rows(fw, imgs):
    fw.write('<div class="row">\n')
    for img in imgs:
        fw.write('  <div class="col-md-3 portfolio-item">\n')
        fw.write('    <a class="fancybox" data-fancybox-group="gallery" href="{{ site.url }}/images/wedding/%s">\n' % img)
        fw.write('      <img class="img-responsive" src="{{ site.url }}/images/wedding/thumb/%s" alt=""/>\n' % img)
        fw.write('    </a>\n')
        fw.write('  </div>\n')

    fw.write('</div>\n<hr/>\n')


def write_paginator(fw, tag, i, num_pages):
    fw.write('<div class="row text-center">\n')
    fw.write('  <div class="col-lg-12">\n')
    fw.write('    <ul class="pagination">\n')
    fw.write('      <li>\n')
    if i == 1:
        fw.write(         '<a href="#">&laquo;</a>\n')
    else:
        fw.write(         '<a href="{{ site.url }}/wedding/%s-%d.html">&laquo;</a>\n' % (tag, i - 1))
    
    n = i / 20
    j_start = n * 20
    if j_start == 0:
        j_start = 1
    
    fw.write('      </li>\n')
    for j in range(j_start, num_pages + 1):
        if j>= j_start + 21:
            break
        if j == i:
            fw.write('      <li class="active">\n')
        else:
            fw.write('      <li>\n')

        fw.write('        <a href="{{ site.url }}/wedding/%s-%d.html">%d</a>\n' % (tag, j, j))
        fw.write('      </li>\n')
    
    fw.write('      <li>\n')
    if i == num_pages:
        fw.write(         '<a href="#">&raquo;</a>\n')
    else:
        fw.write(         '<a href="{{ site.url }}/wedding/%s-%d.html">&raquo;</a>\n' % (tag, i + 1))
    fw.write('      </li>\n')
    fw.write('    </ul>\n')
    fw.write('  </div>\n')
    fw.write('</div>\n<hr>\n')


f = open('list.txt')
tag_photo = {}

for l in f:
    parts = l.strip().split(',')
    photo = parts[0]
    for tag in parts[1:]:
        if tag:
            photos = tag_photo.get(tag, list())
            photos.append(photo)
            tag_photo[tag] = photos

print tag_photo.keys()

for tag, photos in tag_photo.iteritems():
    i = 1
    num_pages = 0
    for page in split_seq(photos, 12):
        num_pages += 1

    for page in split_seq(photos, 12):
        fw = open('%s-%d.html' % (tag, i), 'w')
        write_header(fw, tag)
        for imgs in split_seq(page, 4):
            write_rows(fw, imgs)
        write_paginator(fw, tag, i, num_pages)
        fw.close()
        i += 1

num_pages_all = 0
for tag in ['sbori', 'we', 'priezd', 'ceremony', 'party', 'honeymoon']:
    photos = tag_photo[tag]
    for page in split_seq(photos, 12):
        num_pages_all += 1

c = 1
for tag in ['sbori', 'we', 'priezd', 'ceremony', 'party', 'honeymoon']:
    photos = tag_photo[tag]
    for page in split_seq(photos, 12):
        fw_all = open('all-%d.html' % c, 'w')
        write_header(fw_all, 'all')
        for imgs in split_seq(page, 4):
            write_rows(fw_all, imgs)
        write_paginator(fw_all, 'all', c, num_pages_all)
        fw.close()
        i += 1
        c += 1