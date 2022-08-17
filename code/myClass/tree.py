from io import TextIOWrapper
from ._typing import Tree, Any

class Tree(object):
    """
    The `Tree` class allows the creation of a simple Tree type data structure. The class is main used for representation
    and processing of data from `CibioCM` group of the `University of Trento - Cibio Department`.

    Parameters
    ----------
    name : `str`, default "root", optional
        The name of the tree root. If `name` is `None` then the Tree object is a `None object of Tree`
    counter : `int`, default 0, optional
        Counter of the node used to count how many times the node has been croosed after each addition of a node
        (new or already present).  The `root node`, in particular, contains the sum of the countercords of his children
    parent : `Tree` or `None`, default `itself`, optional
        The parent of the node/tree
    children : `dict`, default `{}`, optional
        The list of children of the tree root
    customVariables : `dict`, optional
        Dictionary where you can insert custom variables to the tree node
    
    Examples
    ----------
    We create a default tree
    >>> tree = mc.Tree("example_name")
    """
    # Tree = object
    def __init__(node, name: str = "root", counter: int = 0, parent: Tree = None, children: dict = None, customVariables: dict = None) -> Tree:
        # assert isinstance(parent, Tree | None)
        if name is None:
            node.name = None
            node.counter = None
            node.parent = None
            node.children = None
            node.customVariables = None
        else:
            node.name = name
            node.counter = counter
            node.parent = node
            node.children = {}
            node.customVariables = {}

    def __repr__(node) -> str:
        if node.name is None:
            return "None"
        else:
            return node.name

    def __eq__(node, __o: object) -> bool:
        return __o.name == node.name

    def __str__(node) -> str:
        if node.name is None:
            return "None"
        else:
            return "name = " + node.name + ", counter = " + str(node.counter) + ", parent = {" + str(node.parent.get_name()) + "}, children = " + str(list(node.children.keys()))
    
    def add_child(node, child: Tree = None, path: list = None, init: bool = False) -> None:
        """
        Adds the child node to the node indicated in the path path or adds the nodes specified by the path path.
        
        Parameters
        ----------
        child : `None` or `Tree`
            Child to be specified in case you want to insert it at the end of the given path.
        path : `list`
            List of strings that specify the various direct ancestors of the node to be inserted or the nodes to be inserted in succession.
            In fact, if not present, the various nodes will be generated in succession until the destination.
        init : `bool`, default `False`, optional
            If specified, it determines how the node is inserted.
            - `False`: Inserts the `child` node at the end of the specified `path`, that is as the child of the last node of the path
            (if intermediate nodes in path are not present, they will be added automatically)
            - `True` : Ignores the `child` parameter and inserts all nodes in `path` if not already present
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree()
        
        We add node `c__XXXX` following the path
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        
        Result:\n
        [1] root\n
        +--> [1] k__XXXX\n
            +------> [1] p__XXXX\n
                +----------> [1] c__XXXX
        
        See Also
        ----------
        print_tree : Shows how the data structure will be displayed
        """
        #assert isinstance(child, Tree | None)
        if node.name is not None:
            if len(path) == 0:
                if child.name not in node.children:
                    child.parent = node
                    node.children[child.name] = child
                    node.inc_counter(child.counter)
            elif (len(path) == 1) and init:
                if path[0] not in node.children:
                    node.children[path[0]] = Tree(path[0], 1, node, {})
                    node.children[path[0]].parent = node
            else:
                if path[0] not in node.children:
                    node.children[path[0]] = Tree(path[0], 0, node, {})
                    node.children[path[0]].parent = node
                node.children[path[0]].add_child(child, path[-(len(path)-1):], init)
            
            if init:
                node.inc_counter()
            else:
                node.inc_counter(node.children[path[0]].counter)
    
    def get_name(node) -> str:
        """
        Get the `name` of the representative of tree, or the root node of the `Tree` object.
        
        Return
        ----------
        str
            Return the string of the name of the `Tree` root node
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree("example_name")
        
        We add node `c__XXXX` following the path
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        
        Now obtain the name of the tree
        >>> tree.get_name()
        'example_name'
        
        See Also
        ----------
        get_counter : Get the `counter` value of the tree root node
        get_parent : Get the `parent` node of this tree
        get_children : Get all `children` of this node of the tree
        """
        return node.name
    
    def get_counter(node) -> int:
        """
        Get the `counter` value of the representative of tree, or the root node of the `Tree` object.
        
        Return
        ----------
        int
            Return the integer of the `Tree` root node
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree("example_name")
        
        We add node `c__XXXX` following the path
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        
        Now obtain the counter of the tree
        >>> tree.get_counter()
        1
        
        See Also
        ----------
        get_name : Get the `name` of the tree root node
        get_parent : Get the `parent` node of this tree
        get_children : Get all `children` of this node of the tree
        """
        return node.counter
    
    def get_parent(node): # -> Tree | None:
        """
        Get the `parent` of the representative of tree, or the root node of the `Tree` object.
        
        Return
        ----------
        Tree
            Return the `Tree` object of the parent of this tree
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree("example_name")
        
        We add node `c__XXXX` following the path
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        
        Now obtain the parent of the tree
        >>> tree.get_children()["k__XXXX"].get_parent()
        k__XXXX
        
        See Also
        ----------
        get_name : Get the `name` of the tree root node
        get_counter : Get the `counter` value of the tree root node
        get_children : Get all `children` of this node of the tree
        """
        return node.parent
    
    def get_children(node) -> dict:
        """
        Get the `children` of the representative of tree, or the root node of the `Tree` object.
        
        Return
        ----------
        dict
            Return the `dictionar` of the node of this tree
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree("example_name")
        
        We add node `c__XXXX` and node `c__YYYY` following the path
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        >>> path = ["k__YYYY", "p__YYYY", "c__YYYY"]
        >>> tree.add_child(path = path, init = True)
        
        Now obtain the parent of the tree
        >>> tree.get_children()
        {'k__XXXX': k__XXXX, 'k__YYYY': k__YYYY}
        
        See Also
        ----------
        get_name : Get the `name` of the tree root node
        get_counter : Get the `counter` value of the tree root node
        get_parent : Get the `parent` node of this tree
        """
        return node.children

    def get_customVariables(node) -> dict:
        """
        Get the custom node variables

        Return
        ----------
        dict
            Return the `dictionar` of the custom variables of node of this tree
        
        See Also
        ----------
        get_name : Get the `name` of the tree root node
        get_counter : Get the `counter` value of the tree root node
        get_parent : Get the `parent` node of this tree
        get_particular_customVariables : Get the custom node variable
        """
        return node.customVariables
    
    def get_particular_customVariables(node, key: str) -> Any:
        """
        Get the custom node variable

        Return
        ----------
        Any
            Return the value of `key` of the custom variables
        
        See Also
        ----------
        get_customVariables : Get the custom node variables
        """
        if (key is not None) and (key in node.customVariables.keys()):
            return node.customVariables[key]

    def get_child(node, path: list): #  -> Tree | None:
        """
        Get the child node to the node indicated in the path.
        
        Parameters
        ----------
        target : `list`
            List of strings that specify the various direct ancestors of the node to be found.
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree()
        
        We add node `c__XXXX` following the path
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        
        Result:\n
        [1] root\n
        +--> [1] k__XXXX\n
            +------> [1] p__XXXX\n
                +----------> [1] c__XXXX
        
        See Also
        ----------
        print_tree : Shows how the data structure will be displayed
        """
        if len(path) == 1:
            return node.children[path[0]]
        elif path[0] in node.children:
            return node.children[path[0]].get_child(path[-(len(path)-1):])
        else:
            return Tree(None)
    
    def get_level(node, level: int = 0, out_file: TextIOWrapper = None) -> Tree:
        """
        Get complete level (all nodes) of this tree.
        
        Parameters
        ----------
        level : `int`, default `0`
            Level of the tree that you want to get. For the taxonomy levels of the SGBs you have:
            - `0` : "Kingdom Level"
            - `1` : "Phylum Level"
            - `2` : "Class Level"
            - `3` : "Order Level"
            - `4` : "Family Level"
            - `5` : "Genus Level"
            - `6` : "Species Level"
            - `7` : "SGB Level"
        out_file : `TextIOWrapper`, default `None`, optional
            If specified, the output will also redirect to the specified file `out_file`.
            - `None`: No particular output
            - `TextIOWrapper object` : The output will also be exported in the file already opened before the method invocation.
        
        Return
        ----------
        Tree
            Return the `Tree` object where:
            - `name` = Level request: <Name of Level>
            - `counter` = the sum of the children's counter
            - `parent` = itself
            - `children` = all node objects in that level
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree()
        
        We add node `c__XXXX` and node `c__YYYY` following the path and print the tree
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        >>> path = ["k__YYYY", "p__YYYY", "c__YYYY"]
        >>> tree.add_child(path = path, init = True)\n
        >>> tree.print_tree()
        [2] root\n
        +--> [1] k__XXXX\n
            +------> [1] p__XXXX\n
                +----------> [1] c__XXXX\n
        +--> [1] k__YYYY\n
            +------> [1] p__YYYY\n
                +----------> [1] c__YYYY\n
        
        Now get the level 1 (Phylum level) and then print its
        >>> tree = tree.get_level(1)
        >>> tree.print_tree()
        [2] Level request: Phylum\n
        +--> [1] p__XXXX\n
            +------> [1] c__XXXX\n
        +--> [1] p__YYYY\n
            +------> [1] c__YYYY\n
        
        See Also
        ----------
        add_child : Add new child
        print_tree : Shows how the data structure will be displayed
        """
        label_l = str(level)
        if level == 0:
            label_l = "Kingdom"
        elif level == 1:
            label_l = "Phylum"
        elif level == 2:
            label_l = "Class"
        elif level == 3:
            label_l = "Order"
        elif level == 4:
            label_l = "Family"
        elif level == 5:
            label_l = "Genus"
        elif level == 6:
            label_l = "Species"
        elif level == 7:
            label_l = "SGB"
        
        res = Tree("Level request: " + label_l)
        
        if level > 0:
            res.children = node.__get_level_rec(level_rec = level, dict = {})
        else:
            res.children = node.children
        
        for i in res.children:
            res.counter += res.children[i].counter
        
        if out_file is not None:
            res.print_tree(file = out_file)
        
        return res
    
    def __get_level_rec(node, level_rec: int = 0, here: int = 0, dict: dict = {}) -> dict:
        for c in node.children:
            if level_rec == here + 1:
                dict.update(node.children[c].get_children())
            else:
                dict.update(node.children[c].__get_level_rec(level_rec, here + 1, dict))
        
        return dict
    
    def get_level_list(node, level: int = 0) -> list:
        """
        Get complete level (all nodes) of this tree in a list.
        
        Parameters
        ----------
        level : `int`, default `0`
            Level of the tree that you want to get. For the taxonomy levels of the SGBs you have:
            - `0` : "Kingdom Level"
            - `1` : "Phylum Level"
            - `2` : "Class Level"
            - `3` : "Order Level"
            - `4` : "Family Level"
            - `5` : "Genus Level"
            - `6` : "Species Level"
            - `7` : "SGB Level"
        
        Return
        ----------
        List
            Return the `list` of al nodes in the specified level. This function is similar to `get_level`
            but will return all nodes (also duplicates). In particular return a `list` of `Tree` objects.
        
        See Also
        ----------
        get_level : Get complete level (all nodes) of tree
        print_tree : Shows how the data structure will be displayed
        """
        res = list()
        
        if level > 0:
            res.extend(node.__get_level_list_rec(level_rec = level, l = list()))
            
        else:
            res.extend(list(node.children.values()))
        
        return res
    
    def __get_level_list_rec(node, level_rec: int = 0, here: int = 0, l: list = list()): # -> list[Tree]:
        for c in node.children:
            if level_rec == here + 1:
                l.extend(list(node.children[c].children.values()))
            else:
                l.extend(node.children[c].__get_level_list_rec(level_rec, here + 1, l))
        
        return l
    
    def get_dict_of_counter(node) -> dict:
        """
        Get a dictionary of all children with their counter from this tree.
        
        Return
        ----------
        dict
            Return the dictionary of all nodes where:
            - `key` is the name of the child
            - `value` is the counter value of the child
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree()
        
        We add node `c__XXXX` and node `c__YYYY` following the path and print the tree
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        >>> path = ["k__YYYY", "p__YYYY", "c__YYYY"]
        >>> tree.add_child(path = path, init = True)\n
        >>> tree.print_tree()
        [2] root\n
        +--> [1] k__XXXX\n
            +------> [1] p__XXXX\n
                +----------> [1] c__XXXX\n
        +--> [1] k__YYYY\n
            +------> [1] p__YYYY\n
                +----------> [1] c__YYYY\n
        
        Get the dictionary
        >>> tree.get_dict_of_counter()
        {'k__XXXX': 1, 'k__YYYY': 1}
        
        See Also
        ----------
        add_child : Add new child
        print_tree : Shows how the data structure will be displayed
        """
        res = dict()
        
        for c in node.children:
            res.update({c : node.children[c].get_counter()})
        
        return res
    
    def inc_counter(node, quantity: int = 1) -> None:
        """
        Increase the tree root counter.
        
        Parameters
        ----------
        quantity : `int`, default `1`, optional
            If specified, the counter will increase of a particolar value.
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree()
        
        We add node `c__XXXX` and node `c__YYYY` following the path and print the tree
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        >>> path = ["k__YYYY", "p__YYYY", "c__YYYY"]
        >>> tree.add_child(path = path, init = True)\n
        >>> tree.print_tree()
        [2] root\n
        +--> [1] k__XXXX\n
            +------> [1] p__XXXX\n
                +----------> [1] c__XXXX\n
        +--> [1] k__YYYY\n
            +------> [1] p__YYYY\n
                +----------> [1] c__YYYY\n
        
        Now increase the counter of tree
        >>> tree.inc_counter()
        >>> tree.get_counter()
        3
        
        Or
        >>> tree.inc_counter()
        >>> tree.get_counter(4)
        6
        
        See Also
        ----------
        add_child : Add new child
        print_tree : Shows how the data structure will be displayed
        get_counter : Get the `counter` value of the tree root node
        """
        node.counter += quantity
    
    def print_tree(node, out_file: TextIOWrapper = None) -> None:
        """
        Print the all tree on `stdout` (default) or on a file specified in `file`.
        
        Parameters
        ----------
        out_file : `TextIOWrapper`, default `None`, optional
            If specified, the output will redirect to the specified file `out_file`.
            - `None`: No particular output
            - `TextIOWrapper object` : The output will be exported in the file already opened before the method invocation.
        
        Examples
        ----------
        We create a default tree
        >>> tree = mc.Tree()
        
        We add node `c__XXXX` and node `c__YYYY` following the path
        >>> path = ["k__XXXX", "p__XXXX", "c__XXXX"]
        >>> tree.add_child(path = path, init = True)
        >>> path = ["k__YYYY", "p__YYYY", "c__YYYY"]
        >>> tree.add_child(path = path, init = True)\n
        
        Now print the tree
        >>> tree.print_tree()
        [2] root\n
        +--> [1] k__XXXX\n
            +------> [1] p__XXXX\n
                +----------> [1] c__XXXX\n
        +--> [1] k__YYYY\n
            +------> [1] p__YYYY\n
                +----------> [1] c__YYYY\n
        
        See Also
        ----------
        add_child : Add new child
        """
        if node.name is not None:
            node.__print_tree_rec(out_file = out_file)
    
    def __print_tree_rec(node, level: int = 0, out_file: TextIOWrapper = None) -> None:
        if out_file is None:
            print("[" + str(node.get_counter()) + "] " + node.name)
            for i in node.children:
                for j in range(0, level):
                    print("\t", end = "")
                print("+--", end = "")
                for j in range(0, level):
                    print("----", end = "")
                print("> ", end = "")
                node.children[i].__print_tree_rec(level+1)
        else:
            out_file.write("[" + str(node.get_counter()) + "] " + node.name + "\n")
            for i in node.children:
                line = ""
                for j in range(0, level):
                    line += "\t"
                line += "+--"
                for j in range(0, level):
                    line += "----"
                line += "> "
                out_file.write(line)
                node.children[i].__print_tree_rec(level+1, out_file)
