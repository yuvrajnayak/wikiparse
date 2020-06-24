import xml.etree.ElementTree as etree
import codecs

total_count = 0
article_count = 0
redirect_count = 0
template_count = 0
title = None


def strip_tag_name(t):
    t = elem.tag
    idx = t.rfind("}")
    if idx != -1:
        t = t[idx + 1:]
    return t


al_writer = codecs.open("output/article_list.txt", "a", "utf-8")
rl_writer = codecs.open("output/redirect_list.txt", "a", "utf-8")
tl_writer = codecs.open("output/template_list.txt", "a", "utf-8")


# change "sample_data.xml" to the path to the wikipedia xml file you want to parse
for event, elem in etree.iterparse("sample_data.xml", events=("start", "end")):
    tname = strip_tag_name(elem.tag)

    if event == "start":
        if tname == "page":
            title = ""
            id = -1
            redirect = ""
            inrevision = False
            ns = 0
        elif tname == "revision":
            inrevision = True
    else:
        if tname == "title":
            title = elem.text
        elif tname == "id" and not inrevision:
            id = int(elem.text)
        elif tname == "redirect":
            redirect = elem.attrib["title"]
        elif tname == "ns":
            ns = int(elem.text)
        elif tname == "page":
            total_count += 1

            if ns == 10:
                template_count += 1
                tl_writer.write(title + " " + str(id) + "\n")
            elif len(redirect) > 0:
                redirect_count += 1
                rl_writer.write(title + " --> " + redirect +
                                " " + str(id) + "\n")
            else:
                article_count += 1
                al_writer.write(title + " " + redirect + " " + str(id) + "\n")

            if total_count > 1 and (total_count % 50000) == 0:
                    print(total_count)

        elem.clear()

print("Total indexed: ", total_count)
print("Articles: ", article_count)
print("Redirects: ", redirect_count)
print("Templates: ", template_count)
