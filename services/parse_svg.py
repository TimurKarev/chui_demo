import xml.etree.ElementTree as ET


class OldSVGParser:

    @staticmethod
    def parse_svg(file_name):
        svg = ET.parse(file_name)

        root = svg.getroot()
        gs = list(root)[-1]
        class_tag = ''
        for g in gs.findall('{http://www.w3.org/2000/svg}g'):
            if len(g.findall('{http://www.w3.org/2000/svg}desc')) > 0:
                desc = g.find('{http://www.w3.org/2000/svg}desc')
                if desc.text == 'ОПИСАНИЕ ПРОБЛЕМЫ/ЗАДАЧИ':
                    path = g.find('{http://www.w3.org/2000/svg}path')
                    class_tag = path.attrib['class']

        print('------------------------------')
        result = []
        if class_tag != '':
            for g in gs.findall('{http://www.w3.org/2000/svg}g'):
                path = g.find('{http://www.w3.org/2000/svg}path')
                if path != None:
                    if path.attrib['class'] == class_tag:
                        current_desk = g.find('{http://www.w3.org/2000/svg}text')
                        txt = ''
                        try:
                            for t in current_desk.itertext():
                                txt += t
                        except:
                            pass
                        if txt != '' and txt != 'ОПИСАНИЕ ПРОБЛЕМЫ/ЗАДАЧИ':
                            result.append(txt)
        return result