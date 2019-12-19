import os, inspect, importlib
import graphviz as gv

class InheritanceTree:
    '''Tree object designed to parse packages and modules for objects mros
    and then create complex graphical visualizations.'''
    
    def __init__(self):
        self.tree = {}
    
    @staticmethod
    def _import_all(base_dir):
        '''Creates an import list where modules can be identified and later scanned.
        Parameters:
        base_dir: str
        The file location for the package, folder, or module to be inspected.
            Accepted format example for windows is "C:\\User\\Packages\\Package"'''

        lst = []
        for item in os.walk(base_dir):
            dirname, folders, files = item

            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    if dirname == loc:
                        file = file[:-3]
                    else:
                        #import folder.module...
                        file = ('.').join(dirname[len(loc):].split(os.path.sep)[1:] + [file[:-3]])
                    lst.append(importlib.import_module(file))
        return lst


    @staticmethod
    def _create_dct(module_name):
        '''Scans a module for classes and creates an mro dictionary for each class.
        Parameters:
        module_name: str
        name of the module being isnpected for base classes.'''

        dct = {}
        members = inspect.getmembers(os.sys.modules[module_name])
        for cls in {cls for name, cls in members if inspect.isclass(cls)}:
            dct[cls.__name__] = {y:x for x,y in enumerate([c.__name__ for c in cls.__bases__])}
        return dct

    
    def create_tree(self, base_dir):
        '''Combines dictionary module mappings to create a single dictionary.
        Parameters:
        base_dir: str
        The desired folder contents to be scanned. 
            This can be single module files or the top-most package folder.'''
        
        dct1 = {}
        for mod in self._import_all(base_dir):
            dct2 = self._create_dct(mod.__name__)
            dct1 = {**dct1, **dct2}
        self.tree = dct1


    def create_graph(self, title_kwargs={}, edge_kwargs={}, node_kwargs={}):
        '''Uses an mro dictionary (self.tree) to create a graphical tree visualization using graphviz.
        Accepts kwargs as dict for graphviz customization.
        Parameters:
        title_kwargs: dict
        The customization kwargs for graphviz graph object.

        edge_kwargs: dict
        The customization kwargs for graph edges.

        node_kwargs: dict
        The customization kwargs for graph nodes.'''

        if 'name' not in title_kwargs:
            title_kwargs['name'] = 'MRO'
        if 'format' not in title_kwargs:
            title_kwargs['format'] = 'png'
        if 'color' in edge_kwargs:
            color = edge_kwargs.pop('color')
        else:
            color = 'black'

        g = gv.Digraph(**title_kwargs)

        #unpack key:value pairs and create nodes and edges
        for k in self.tree:
            g.node(k, **node_kwargs)
            for v in self.tree[k]:
                #Indicate inheritance order by number of edge lines
                single = [color]
                single.extend([f'invis:{color}']*(self.tree[k][v]))
                w = (':').join(single)
                g.edge(v, k, color=w, **edge_kwargs)

        self.graph = g
        return g
