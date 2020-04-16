from lxml import etree as ET

def clear():
    NclEntity.IDS = {}

class ImportedBase:
    RULE_BASE = 0
    TRANSITION_BASE = 1
    REGION_BASE = 2
    DESCRIPTOR_BASE = 3
    CONNECTOR_BASE = 4
    
    def __init__(self, alias, documentURI, region=None, baseId=None, base_type=None):
        self.alias = alias
        self.documentURI = documentURI
        self.region = region
        self.baseId = baseId
        self.base_type = base_type
        
    def to_xml(self, xml_base):
        xml_imported_base = ET.SubElement(xml_base, 'importBase', 
                                          alias=self.alias, 
                                          documentURI=self.documentURI)
        
        if self.region != None:
            xml_imported_base.attrib['region'] = self.region.id
            
        if self.baseId != None:
            xml_imported_base.attrib['baseId'] = self.baseId
        

class NclDocument:
    def __init__(self, mid, bodyid=None):
        self.id = mid
        self.region_base = []
        self.descriptor_base = []
        self.connector_base = []
        self.transition_base = []
        self.bodyid = bodyid
        
        self.body = None
        self.__imported_connectors_base = []
        self.__imported_descriptors_base = []
        self.__imported_regions_base = []
        self.__aliases = {}
        self.__elements = {}
        
    def add_imported_connector_base(self, imported_base):
        imported_base.base_type = ImportedBase.CONNECTOR_BASE
        self.__imported_connectors_base.append(imported_base)
        self.__aliases[imported_base.alias] = imported_base
        
    def dump(self):
        xml_doc = self.__to_xml()
        return ET.tostring(xml_doc, pretty_print=True)
        
    
    def dump_file(self, filename):
        xml_file = open(filename, 'w+')
        xml_doc = self.__to_xml()
        root = xml_doc.getroottree()
        root.write(xml_file,  encoding="ISO-8859-1", pretty_print=True, xml_declaration=True)
    
    def __to_xml(self):
        xml_doc = ET.Element('ncl', id=self.id, xmlns="http://www.ncl.org.br/NCL3.0/EDTVProfile")
        self.__head_to_xml(xml_doc)
        self.__body_to_xml(xml_doc)
        return xml_doc
        
    def __head_to_xml(self, xml_doc):
        xml_head = ET.SubElement(xml_doc, "head")
        if len(self.region_base) > 0 or len(self.__imported_regions_base) > 0:
            xml_base = ET.SubElement(xml_head, "regionBase")
            for region in self.region_base:
                region.to_xml(xml_base)
                
            for imported_base in self.__imported_regions_base:
                imported_base.to_xml(xml_base)
                
        if len(self.region_base) > 0 or len(self.__imported_descriptors_base) > 0:
            xml_base = ET.SubElement(xml_head, "descriptorBase")
            for descriptor in self.descriptor_base:
                descriptor.to_xml(xml_base)
                
            for imported_base in self.__imported_descriptors_base:
                imported_base.to_xml(xml_base)
                
        if len(self.connector_base) > 0 or len(self.__imported_connectors_base) > 0:
            xml_base = ET.SubElement(xml_head, "connectorBase")
            for connector in self.connector_base:
                connector.to_xml(xml_base)
                
            for imported_base in self.__imported_connectors_base:
                imported_base.to_xml(xml_base)
                
    def add_node(self, node):
        if self.body == None:
            self.body = Context(self.bodyid, True)
            
        self.body.add_node(node)
    
    def add_anchor(self, anchor):
        if self.body == None:
            self.body = Context(self.bodyid, True)
            
        self.body.add_anchor(anchor)
    
    def add_link(self, link):
        if self.body == None:
            self.body = Context(self.bodyid, True)
            
        self.body.add_link(link)
                    
    def __body_to_xml(self, xml_doc):
        if self.body != None:
            self.body.to_xml(xml_doc)
        
        
        

class NclEntity:
    IDS = {}
    def __init__(self, mid=None, missing_id=None):
        if missing_id == True:
            mid = NclEntity.generate_id()
        elif self.IDS.has_key(mid):
            raise ValueError("The NclEntity id must be unique in a NCL document: " + mid)    
        self.id = mid
        self.IDS[mid] = self
        self.missing_id = missing_id
        
    @staticmethod
    def generate_id():
        import uuid
        return str(uuid.uuid4())
    
    def to_xml(self, parent_node):
        pass

class Region(NclEntity):
    def __init__(self, mid, width=None, height=None, top=None, left=None, right=None, \
                 bottom=None, zIndex=None, title=None):
        
        NclEntity.__init__(self, mid)
        self.width = width
        self.height = height
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.zIndex = zIndex
        self.title = title
        self.regions = []
        
    def add_region(self, region):
        self.regions.append(region)
        
    def to_xml(self, xml_root):
        
        xml_region = ET.SubElement(xml_root, 'region', id=self.id)
        if self.width != None:
            xml_region.attrib['width'] = str(self.width)
        if self.height != None:
            xml_region.attrib['height'] = str(self.height)
        if self.top != None:
            xml_region.attrib['top'] = str(self.top)
        if self.left != None:
            xml_region.attrib['left'] = str(self.left)
        if self.right != None:
            xml_region.attrib['right'] = str(self.right)
        if self.bottom != None:
            xml_region.attrib['bottom'] = str(self.bottom)
        if self.zIndex != None:
            xml_region.attrib['zIndex'] = str(self.zIndex)
        if self.title != None:
            xml_region.attrib['title'] = self.title
            
        
        for subregion in self.regions:
            subregion.to_xml(xml_region)
        
        return xml_region        

class Descriptor(NclEntity):
    def __init__(self, mid, player=None, explicitDur=None, \
                           region=None, freeze=None, moveLeft=None, moveRight=None, \
                           moveUp=None, moveDown=None, focusIndex=None, \
                           focusBorderColor=None, focusBorderWidth=None, \
                           focusBorderTransparency=None, focusSrc=None, \
                           focusSelSrc=None, selBorderColor=None, transIn=None, transOut=None):
        
        NclEntity.__init__(self, mid)
        self.player = player
        self.explicitDur = explicitDur
        if isinstance(region, str):
            region = NclEntity.IDS[region]
        if region != None and not isinstance(region, Region):
            raise TypeError('The region argument must be an instance of Region or' + 
                            ' the id of a valid Region instance')
        
        self.region = region
        self.freeze = freeze
        self.moveLeft = moveLeft
        self.moveRight = moveRight
        self.moveUp = moveUp
        self.moveDown = moveDown
        self.focusIndex = focusIndex
        self.focusBorderColor = focusBorderColor
        self.focusBorderWidth = focusBorderWidth
        self.focusBorderTransparency = focusBorderTransparency
        self.focusSrc = focusSrc
        self.focusSelSrc = focusSelSrc
        self.selBorderColor = selBorderColor
        self.transIn = transIn
        self.transOut = transOut
        self.__descriptor_params = {}
        
    def add_transIn(self, transition):
        if self.transIn == None:
            self.transIn = []
        self.transIn.append(transition)
        
    def add_transOut(self, transition):
        if self.transOut == None:
            self.transOut = []
        self.transOut.append(transition)
        
    def add_param(self, name, value):
        self.__descriptor_params[name] = value
        
    def to_xml(self, xml_root):
        xml_descriptor = ET.SubElement(xml_root, 'descriptor', id=self.id)
        
        if self.player != None:
            xml_descriptor.attrib['player'] = str(self.player)
        
        if self.explicitDur != None:
            xml_descriptor.attrib['explicitDur'] = str(self.explicitDur)
        
        if self.region != None:
            xml_descriptor.attrib['region'] = self.region.id
            
        if self.freeze != None:
            xml_descriptor.attrib['freeze'] = str(self.freeze).lower()
            
        if self.moveLeft != None:
            xml_descriptor.attrib['moveLeft'] = self.moveLeft
        
        if self.moveRight != None:
            xml_descriptor.attrib['moveRight'] = self.moveRight
        
        if self.moveUp != None:
            xml_descriptor.attrib['moveUp'] = self.moveUp
            
        if self.moveDown != None:
            xml_descriptor.attrib['moveDown'] = self.moveDown
            
        if self.focusIndex != None:
            xml_descriptor.attrib['focusIndex'] = self.focusIndex
            
        if self.focusBorderColor != None:
            xml_descriptor.attrib['focusBorderColor'] = self.focusBorderColor
            
        if self.focusBorderWidth != None:
            xml_descriptor.attrib['focusBorderWidth'] = str(self.focusBorderWidth)
            
        if self.focusBorderTransparency != None:
            xml_descriptor.attrib['focusBorderTransparency'] = str(self.focusBorderTransparency)
            
        if self.focusSrc != None:
            xml_descriptor.attrib['focusSrc'] = self.focusSrc
            
        if self.focusSelSrc != None:
            xml_descriptor.attrib['focusSelSrc'] = self.focusSelSrc
            
        if self.selBorderColor != None:
            xml_descriptor.attrib['selBorderColor'] = self.selBorderColor
            
        if self.transIn != None and len(self.transIn) > 0:
            tmpstr = ""
            for transition in self.transIn:
                tmpstr = tmpstr + transition.id
            xml_descriptor.attrib['transIn'] = tmpstr
            
        if self.transOut != None and len(self.transOut) > 0:
            tmpstr = ""
            for transition in self.transOut:
                tmpstr = tmpstr + transition.id
            xml_descriptor.attrib['transOut'] = tmpstr
        
        for name, value in self.__descriptor_params.items():
            ET.SubElement(xml_root, 'descriptorParam', name=name, value=value)
        

class Connector(NclEntity):
    pass

class Transition(NclEntity):
    pass

class Node(NclEntity):
    def __init__(self, mid):
        NclEntity.__init__(self, mid)
        self.__anchors = []
    
    def add_anchor(self, anchor):
        if not isinstance(anchor, Anchor):
            raise TypeError('The argument must be an instance of Anchor    ')
        self.__anchors.append(anchor)
        
    def get_anchors(self):
        return self.__anchors

class Context(Node):
    def __init__(self, mid, is_body=None, refer=None):
        Node.__init__(self, mid)
        self.is_body = is_body
        if refer == None:
            self.refer = None
        elif isinstance(refer, str):
            self.refer = NclEntity.IDS[refer]
        elif isinstance(refer, Context):
            self.refer = refer
        else:
            raise TypeError('The refer argument must be an instance ' + \
                            'of Context or the id of a valid Context instance')
        self.__nodes = []
        self.__links = []
        
    def add_node(self, node):
        if not isinstance(node, Node):
            raise TypeError('The argument must be an instance of Node')
        self.__nodes.append(node)
        
    def add_link(self, link):
        if not isinstance(link, Link):
            raise TypeError('The argument must be an instance of Link')
        self.__links.append(link)
        
    def add_anchor(self, anchor):
        if not isinstance(anchor, Port) and not isinstance(anchor, NodeProperty):
            raise TypeError('The argument must be an instance of Port or NodeProperty')
        Node.add_anchor(self, anchor)
        
    def to_xml(self, xml_root):
        xml_context = None
        if self.is_body == True:
            xml_context = ET.SubElement(xml_root, 'body')
            if self.id != None:
                xml_context.attrib['id'] = self.id
        else:
            xml_context = ET.SubElement(xml_root, 'context', id=self.id)
            
        if self.refer != None:
            xml_context.attrib['refer'] = self.refer.id     
            
        for anchor in self.get_anchors():
            anchor.to_xml(xml_context)
            
        for node in self.__nodes:
            node.to_xml(xml_context)
    
        for link in self.__links:
            link.to_xml(xml_context)

class Media(Node):
    __instance_types = ['new', 'instSame', 'gradSame']
        
    def __init__(self, mid=None, src=None, mtype=None, refer=None, instance=None, descriptor=None):
        Node.__init__(self, mid)
        self.src = src
        self.type = mtype
        if refer == None:
            self.refer = None
        elif isinstance(refer, str):
            self.refer = NclEntity.IDS[refer]
        elif isinstance(refer, Media):
            self.refer = refer
        else:
            raise TypeError('The refer argument must be an instance ' + \
                            'of Media or the id of a valid Media instance')
            
        if instance != None and instance not in self.__instance_types:
            raise ValueError('The instance argument must assume the following values: ' + \
                                 str(self.__instance_types))
        self.instance = instance
        if descriptor == None:
            self.descriptor = None
        elif isinstance(descriptor, str):
            self.descriptor = NclEntity.IDS[descriptor]
        elif isinstance(descriptor, Descriptor):
            self.descriptor = descriptor
        else:
            raise TypeError('The descriptor argument must be an instance ' + \
                            'of Descriptor or the id of a valid Descriptor instance')
            
    def add_anchor(self, anchor):
        if not isinstance(anchor, Area) and not isinstance(anchor, NodeProperty):
            raise TypeError('The argument must be an instance of Area or NodeProperty')
        Node.add_anchor(self, anchor)      
        
    def to_xml(self, parent_node):
        xml_media = ET.SubElement(parent_node, 'media')
        xml_media.attrib['id'] = self.id
        
        if self.type != None:
            xml_media.attrib['type'] = self.type
        if self.src != None:
            xml_media.attrib['src'] = self.src
        if self.refer != None:
            xml_media.attrib['refer'] = self.refer.id
        if self.instance != None:
            xml_media.attrib['instance'] = self.instance
        if self.descriptor != None:
            xml_media.attrib['descriptor'] = self.descriptor.id
            
        for anchor in self.get_anchors():
            anchor.to_xml(xml_media)
        

class Anchor(NclEntity):
    def __init__(self, mid, missing_id=None):
        NclEntity.__init__(self, mid, missing_id)

class Port(Anchor):
    def __init__(self, mid, component, interface=None):
        NclEntity.__init__(self, mid)
        
        if isinstance(component, str):
            self.component = NclEntity.IDS[component]
        elif isinstance(component, Node):
            self.component = component
        else:
            raise TypeError('The component argument must be an instance ' + \
                            'of Node or the id of a valid Node instance')
        if interface == None:
            self.interface = None
        elif isinstance(interface, str):
            self.interface = NclEntity.IDS[interface]
        elif isinstance(interface, Anchor):
            self.interface = interface
        else:
            raise TypeError('The interface argument must be an instance ' + \
                            'of Anchor or the id of a valid Anchor instance')
            
    def to_xml(self, parent_node):
        xml_context = ET.SubElement(parent_node, 'port')
        if self.id != None:
            xml_context.attrib['id'] = self.id
        if self.component != None:
            xml_context.attrib['component'] = self.component.id
        if self.interface != None:
            xml_context.attrib['interface'] = self.interface.id

class NodeProperty(Anchor):
    def __init__(self, name, value=None, externable=None):
        Anchor.__init__(self, None, True)
        self.name = name
        self.value = value
        if externable != None and not isinstance(externable, bool):
            raise TypeError('The externable argument must be a bool')
        self.externable = externable
        
    def to_xml(self, parent_node):
        xml_media = ET.SubElement(parent_node, 'property')
        xml_media.attrib['name'] = self.name
        
        if self.value != None:
            xml_media.attrib['value'] = self.value
        if self.externable != None:
            xml_media.attrib['externable'] = str(self.externable).lower()
        

class Area(Anchor):
    def __init__(self, mid, coords=None, begin=None, end=None, beginText=None, 
                 endText=None, beginPosition=None, endPosition=None, first=None, 
                 last=None, label=None, clip=None):
        
        Anchor.__init__(self, mid)
        
        #TODO Check the Area possible arguments value
        self.coords = coords
        self.begin = begin
        self.end = end
        self.beginText = beginText
        self.endText = endText
        self.beginPosition = beginPosition
        self.endPosition = endPosition
        self.first = first
        self.last = last
        self.label = label
        self.clip = clip
        
    def to_xml(self, parent_node):
        xml_media = ET.SubElement(parent_node, 'area')
        xml_media.attrib['id'] = self.id
        
        #TODO More meaningful values for coords, first and last
        if self.coords != None:
            xml_media.attrib['coords'] = self.coords
        if self.begin != None:
            if isinstance(self.begin, str):
                xml_media.attrib['begin'] = self.begin
            else:
                xml_media.attrib['begin'] = str(self.begin) + 's'
        if self.end != None:
            if isinstance(self.end, str):
                xml_media.attrib['end'] = self.end
            else:
                xml_media.attrib['end'] = str(self.end) + 's'
        if self.beginText != None:
            xml_media.attrib['beginText'] = self.beginText
        if self.endText != None:
            xml_media.attrib['endText'] = str(self.endText)
        if self.beginPosition != None:
            xml_media.attrib['beginPosition'] = str(self.beginPosition)
        if self.endPosition != None:
            xml_media.attrib['endPosition'] = str(self.endPosition)
        if self.first != None:
            xml_media.attrib['first'] = self.first
        if self.last != None:
            xml_media.attrib['last'] = self.last
        if self.label != None:
            xml_media.attrib['label'] = self.label
        if self.clip != None:
            xml_media.attrib['clip'] = self.clip

class Link(NclEntity):
    def __init__(self, xconnector, mid=None):
        missing_id = False
        if mid == None:
            missing_id = True
            
        NclEntity.__init__(self, mid, missing_id)
        
        self.__use_alias = False
        if isinstance(xconnector, str):
            if xconnector.count('#'):
                self.__use_alias = True
                self.__xconnector = xconnector
            else:
                self.__xconnector = NclEntity.IDS[xconnector]
        elif isinstance(xconnector, Connector):
            self.__xconnector = xconnector
        else:
            raise TypeError('The xconnector argument must be an instance ' + \
                            'of Connector or the id of a valid xconnector instance')
        
        self.__binds = []
        self.__params = {}
        
    def add_bind(self, bind):
        if not isinstance(bind, Bind):
            raise TypeError('The argument must be an instance of Bind')
        self.__binds.append(bind)
    
    def add_param(self, name, value):
        self.__params[name] = value
        
    def to_xml(self, parent_node):
        xml_link = ET.SubElement(parent_node, 'link')
        if self.__use_alias:
            xml_link.attrib['xconnector'] = self.__xconnector
        else:
            xml_link.attrib['xconnector'] = self.__xconnector.id
            
        if not self.missing_id:
            xml_link.attrib['id'] = self.id
        
        for n, v in self.__params.items():
            ET.SubElement(xml_link, 'linkParam', name=n, value=v)
            
        for bind in self.__binds:
            bind.to_xml(xml_link)
        
class Bind():
    def __init__(self, role, component, interface=None, descriptor=None):
        self.role = role
        
        if isinstance(component, str):
            self.component = NclEntity.IDS[component]
        elif isinstance(component, Node):
            self.component = component
        else:
            raise TypeError('The component argument must be an instance ' + \
                            'of Node or the id of a valid Node instance')
        if interface == None:
            self.interface = None
        elif isinstance(interface, str):
            try:
                self.interface = NclEntity.IDS[interface].id
            except:
                self.interface = interface
        elif isinstance(interface, Anchor):
            self.interface = interface.id
        else:
            raise TypeError('The interface argument must be an instance ' + \
                            'of Anchor or the id of a valid Anchor instance')
            
        if descriptor == None:
            self.descriptor = None
        elif isinstance(descriptor, str):
            self.descriptor = NclEntity.IDS[descriptor]
        elif isinstance(descriptor, Descriptor):
            self.descriptor = descriptor
        else:
            raise TypeError('The descriptor argument must be an instance ' + \
                            'of Descriptor or the id of a valid Descriptor instance')
        
        
        self.__params = {}
        
    def add_param(self, name, value):
        self.__params[name] = value
    
    def to_xml(self, xml_link):
        xml_bind = ET.SubElement(xml_link, 'bind', role=self.role)
        xml_bind.attrib['component'] = self.component.id
        if self.interface != None:
            xml_bind.attrib['interface'] = self.interface
        if self.descriptor != None:
            xml_bind.attrib['descriptor'] = self.descriptor.id
            
        for n, v in self.__params.items():
            ET.SubElement(xml_bind, 'bindParam', name=n, value=v)
    
            

def test():
    ncldoc = NclDocument('nclTest')
    
    ############# REGION BASE #############
    # Fullscreen region
    region = Region('rFullScreen', zIndex=0, width=1400, height=900)
    ncldoc.region_base.append(region)

    # rMainVideo
    sub_region = Region('rMainVideo', zIndex=3, left=91, top=17, width=1218, height=685)
    region.add_region(sub_region)
    # rBgMainVideo
    sub_region = Region('rBgMainVideo', zIndex=2, left=91, top=17, width=1218, height=685)
    region.add_region(sub_region)
    # rBtnMainVideo
    sub_region = Region('rBtnMainVideo', zIndex=5, left=91, top=17, width=1218, height=685)
    region.add_region(sub_region)
    
    # rBtnMainVideo
    sub_region = Region('rMiniVideo1', zIndex=3, left=492, top=733, width=245, height=138)
    region.add_region(sub_region)
    # rBtnMainVideo
    sub_region = Region('rBgMiniVideo1', zIndex=2, left=492, top=733, width=245, height=138)
    region.add_region(sub_region)
    # rBtnMainVideo
    sub_region = Region('rBtnMiniVideo1', zIndex=5, left=492, top=733, width=245, height=138)
    region.add_region(sub_region)
    
    # rMiniVideo2
    sub_region = Region('rMiniVideo2', zIndex=3, left=782, top=733, width=245, height=138)
    region.add_region(sub_region)
    # rBgMiniVideo2
    sub_region = Region('rBgMiniVideo2', zIndex=2, left=782, top=733, width=245, height=138)
    region.add_region(sub_region)
    # rBtnMiniVideo2
    sub_region = Region('rBtnMiniVideo2', zIndex=5, left=782, top=733, width=245, height=138)
    region.add_region(sub_region)
    
    # rMiniVideo3
    sub_region = Region('rMiniVideo3', zIndex=3, left=1072, top=733, width=245, height=138)
    region.add_region(sub_region)
    # rBgMiniVideo3
    sub_region = Region('rBgMiniVideo3', zIndex=2, left=1072, top=733, width=245, height=138)
    region.add_region(sub_region)
    # rBtnMiniVideo3
    sub_region = Region('rBtnMiniVideo3', zIndex=5, left=1072, top=733, width=245, height=138)
    region.add_region(sub_region)
    
    # rBtnStartPause
    sub_region = Region('rBtnStartPause', zIndex=1, left=66, top=729, width=65, height=42)
    region.add_region(sub_region)
    # rBtnStop
    sub_region = Region('rBtnStop', zIndex=1, left=131, top=729, width=58, height=42)
    region.add_region(sub_region)
    # rBtnResize
    sub_region = Region('rBtnResize', zIndex=1, left=189, top=729, width=70, height=42)
    region.add_region(sub_region)
    
    # rBtnPrevious
    sub_region = Region('rBtnPrevious', zIndex=1, left=264, top=727, width=61, height=72)
    region.add_region(sub_region)
    # rBtnBack
    sub_region = Region('rBtnBack', zIndex=1, left=325, top=727, width=67, height=72)
    region.add_region(sub_region)
    # rBtnNext
    sub_region = Region('rBtnNext', zIndex=1, left=392, top=727, width=57, height=72)
    region.add_region(sub_region)
    
    # rTimeBox
    sub_region = Region('rTimeBox', zIndex=0, left=66, top=776, width=191, height=22)
    region.add_region(sub_region)
    # rLua
    sub_region = Region('rLua', zIndex=1, left=66, top=776, width=191, height=22)
    region.add_region(sub_region)
    
    # rModulo
    sub_region = Region('rModulo', zIndex=1, left=62, top=804, width=78, height=23)
    region.add_region(sub_region)
    # rPoi1
    sub_region = Region('rPoi1', zIndex=1, left=138, top=804, width=78, height=23)
    region.add_region(sub_region)
    # rPoi2
    sub_region = Region('rPoi2', zIndex=1, left=214, top=804, width=78, height=23)
    region.add_region(sub_region)
    # rPoi3
    sub_region = Region('rPoi3', zIndex=1, left=292, top=804, width=78, height=23)
    region.add_region(sub_region)
    # rPoi4
    sub_region = Region('rPoi4', zIndex=1, left=369, top=804, width=78, height=23)
    region.add_region(sub_region)
    
    # rDummyFocus
    sub_region = Region('rDummyFocus', zIndex=6, left=0, top=0, width=1, height=1)
    region.add_region(sub_region)
    
    ############# DESCRIPTOR BASE #############
    descriptor = Descriptor('dBackground', region=NclEntity.IDS['rFullScreen'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Main Video
    descriptor = Descriptor('dMainVideo', region=NclEntity.IDS['rMainVideo'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBgMainVideo', region=NclEntity.IDS['rBgMainVideo'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBtnMainVideo', region=NclEntity.IDS['rBtnMainVideo'],
                            focusIndex="iMainVideo", focusBorderWidth=3)
    ncldoc.descriptor_base.append(descriptor)
    
    #Mini Video 1
    descriptor = Descriptor('dMiniVideo1', region=NclEntity.IDS['rMiniVideo1'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBgMiniVideo1', region=NclEntity.IDS['rMiniVideo1'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBtnMiniVideo1', region=NclEntity.IDS['rBtnMiniVideo1'],
                            focusIndex="iMiniVideo1", focusBorderWidth=3)
    ncldoc.descriptor_base.append(descriptor)
    
    #Mini Video 2
    descriptor = Descriptor('dMiniVideo2', region=NclEntity.IDS['rMiniVideo2'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBgMiniVideo2', region=NclEntity.IDS['rMiniVideo2'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBtnMiniVideo2', region=NclEntity.IDS['rBtnMiniVideo2'],
                            focusIndex="iMiniVideo2", focusBorderWidth=3)
    ncldoc.descriptor_base.append(descriptor)
    
    #Mini Video 3
    descriptor = Descriptor('dMiniVideo3', region=NclEntity.IDS['rMiniVideo3'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBgMiniVideo3', region=NclEntity.IDS['rMiniVideo3'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBtnMiniVideo3', region=NclEntity.IDS['rBtnMiniVideo3'],
                            focusIndex="iMiniVideo3", focusBorderWidth=3)
    ncldoc.descriptor_base.append(descriptor)
    
    #Btn Previous
    descriptor = Descriptor('dBtnPrevious', region=NclEntity.IDS['rBtnPrevious'], focusIndex="iPrevious",
                            focusBorderWidth=0, focusSrc="images/btn_previous_hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBtnPreviousDisabled', region=NclEntity.IDS['rBtnPrevious'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Btn Next
    descriptor = Descriptor('dBtnBack', region=NclEntity.IDS['rBtnBack'], focusIndex="iBack",
                            focusBorderWidth=0, focusSrc="images/btn_back_hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBtnBackDisabled', region=NclEntity.IDS['rBtnBack'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Btn Back
    descriptor = Descriptor('dBtnNext', region=NclEntity.IDS['rBtnNext'], focusIndex="iNext",
                            focusBorderWidth=0, focusSrc="images/btn_next_hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dBtnNextDisabled', region=NclEntity.IDS['rBtnNext'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Lua timer
    descriptor = Descriptor('dTimeBox', region=NclEntity.IDS['rTimeBox'])
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dLua', region=NclEntity.IDS['rLua'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Poi Modulo
    descriptor = Descriptor('dPoiModulo', region=NclEntity.IDS['rModulo'], focusIndex="iModulo",
                            focusBorderWidth=0, focusSrc="images/modulo_hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dPoiModuloSelected', region=NclEntity.IDS['rModulo'],
                            focusBorderWidth=0, focusIndex="iModuloSelected")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dPoiModuloDisabled', region=NclEntity.IDS['rModulo'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Poi Slide
    descriptor = Descriptor('dPoiSlide', region=NclEntity.IDS['rPoi1'], focusIndex="iSlide",
                            focusBorderWidth=0, focusSrc="images/slide_hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dPoiSlideSelected', region=NclEntity.IDS['rPoi1'],
                            focusBorderWidth=0, focusIndex="iSlideSelected")
    descriptor = Descriptor('dPoiSlideDisabled', region=NclEntity.IDS['rPoi1'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Poi close
    descriptor = Descriptor('dPoiClose', region=NclEntity.IDS['rPoi2'], focusIndex="iClose",
                            focusBorderWidth=0, focusSrc="images/close_hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dPoiCloseSelected', region=NclEntity.IDS['rPoi2'],
                            focusBorderWidth=0, focusIndex="iCloseSelcted")
    descriptor = Descriptor('dPoiCloseDisabled', region=NclEntity.IDS['rPoi2'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Poi Tela
    descriptor = Descriptor('dPoiTela', region='rPoi3', focusIndex="iTela",
                            focusBorderWidth=0, focusSrc="images/tela_hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dPoiTelaSelected', region=NclEntity.IDS['rPoi3'],
                            focusBorderWidth=0, focusIndex="iTelaSelcted")
    descriptor = Descriptor('dPoiTelaDisabled', region=NclEntity.IDS['rPoi3'])
    ncldoc.descriptor_base.append(descriptor)
    
    #Poi Voz
    descriptor = Descriptor('dPoiVoz', region=NclEntity.IDS['rPoi4'], focusIndex="iVoz",
                            focusBorderWidth=0, focusSrc="images/voz    _hover.png")
    ncldoc.descriptor_base.append(descriptor)
    descriptor = Descriptor('dPoiVozSelected', region=NclEntity.IDS['rPoi4'],
                            focusBorderWidth=0, focusIndex="iVozSelcted")
    descriptor = Descriptor('dPoiVozDisabled', region=NclEntity.IDS['rPoi4'])
    ncldoc.descriptor_base.append(descriptor)
    
    imported_base = ImportedBase('conn', 'connBase.ncl')
    ncldoc.add_imported_connector_base(imported_base)
    
    media = Media('settings', mtype="application/x-ginga-settings")
    media.add_anchor(NodeProperty("service.currentFocus", "0"))
    media.add_anchor(NodeProperty("faceCurrentAnchor", "0"))
    media.add_anchor(NodeProperty("slidesCurrentAnchor", "0"))
    media.add_anchor(NodeProperty("telaCurrentAnchor", "0"))
    media.add_anchor(NodeProperty("vozCurrentAnchor", "0"))
    media.add_anchor(NodeProperty("fullscreenVideo", "None"))
    media.add_anchor(NodeProperty("currentPoiType", "module"))
    ncldoc.add_node(media)
    
    context = Context("module01")
    ncldoc.add_node(context)
    
    port = Port("pModule01", component=context)
    ncldoc.add_anchor(port)
    
    media = Media("video0", src="videos/video_orc.mp4", descriptor="dMainVideo")
    context.add_node(media)
    
    media.add_anchor(NodeProperty(name="bounds"))
    media.add_anchor(NodeProperty(name="visible"))
    media.add_anchor(Area("begin_video1", begin=0))
    
    media.add_anchor(Area("video1_slide_01", begin=0.5))
    media.add_anchor(Area("video1_slide_02", begin=30))
    media.add_anchor(Area("video1_slide_03", begin=42.08))
    media.add_anchor(Area("video1_slide_04", begin=160))
    
    media.add_anchor(Area("video1_face_01", begin=17.9166666667))
    media.add_anchor(Area("video1_face_02", begin=59.1666666667))
    
    media.add_anchor(Area("video1_tela_01", begin=84.1666666667))
    media.add_anchor(Area("video1_tela_02", begin=90.8333333333))
    media.add_anchor(Area("video1_tela_03", begin=98.75))
    media.add_anchor(Area("video1_tela_04", begin=112.916666667))
    media.add_anchor(Area("video1_tela_05", begin=130.833333333))
    media.add_anchor(Area("video1_tela_06", begin=140.416666667))
    
    media = Media("module01Settings", refer="settings", instance="instSame")
    context.add_node(media)
    
    link = Link(xconnector="conn#onSelectionSetStopStart")
    context.add_link(link)
    link.add_bind(Bind(role="onSelection", component="video0", interface="video1_slide_01"))
    bind = Bind(role="set", component="module01Settings", interface="service.currentFocus")
    link.add_bind(bind)
    bind.add_param("setValue", "slide")
    
    ncldoc.dump_file('main.ncl')
    
if __name__ == "__main__":
    test()
    