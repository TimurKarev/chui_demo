import xml.etree.ElementTree as ET


class SVGParser:
    problem_tag = 'проблема'
    problem_pattern_val = 'проблема'

    def __init__(self, file_name):
        svg = ET.parse(file_name)
        root = svg.getroot()
        prefix = root.tag.split('}')[0] + '}'

        foregroundPage = None
        for g in root.findall(f'{prefix}g'):
            for key, value in g.attrib.items():
                if value == 'foregroundPage':
                    foregroundPage = g
                    break

        pattern = []
        for g in foregroundPage:
            for t in g:
                if self.get_clear_tag(t.tag) == 'userDefs':
                    for u in t:
                        if self.get_clear_tag(u.tag) == 'ud':
                            for k, v in u.attrib.items():
                                if v.lower().find(self.problem_tag.lower()) > -1:
                                    pattern.append(g)

        self.result = []
        for pat in pattern:
            g_tup = self.parse_g(pat)
            if g_tup[0] == '0' and g_tup[1].lower() == self.problem_pattern_val.lower():
                pass
            else:
                self.result.append(g_tup)

    def get_clear_tag(self, tag: str):
        return tag.split('}')[1]

    def get_text_from_g(self, g):
        text = None
        for t in g:
            if self.get_clear_tag(t.tag) == 'text':
                text = ''.join(list(t.itertext()))
        return text

    def get_text_and_index_from_g(self, gs):
        txt_g = []
        for g in gs:
            if self.get_clear_tag(g.tag) == 'g':
                for t in g:
                    if self.get_clear_tag(t.tag) == 'text':
                        txt_g.append(g)
        index = ' '
        try:
            index = self.get_text_from_g(txt_g[0])
        except:
            pass

        value = ' '
        try:
            value = self.get_text_from_g(txt_g[-1])
        except:
            pass
        return index, value

    def parse_g(self, gs):
        num_g = 0
        num_text = 0
        for g in gs:
            if self.get_clear_tag(g.tag) == 'g':
                num_g += 1
            if self.get_clear_tag(g.tag) == 'text':
                num_text += 1
        if num_g == 0 and num_text == 1:
            return ' ', self.get_text_from_g(gs)
        if num_g > 0 and num_text == 0:
            return self.get_text_and_index_from_g(gs)