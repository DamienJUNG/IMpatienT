from dash import html,Output,Input,MATCH,State,clientside_callback,dcc,ALL,ClientsideFunction
import uuid
import components
import components.collapse_tree_node

class CollapseTreeRootAIO(html.Div):
    class ids:
        div = lambda aio_ids:{
            'component':'CollapseTreeRootAIO',
            'subcomponent':'div',
            'aio_ids':aio_ids
        }
        store = lambda aio_ids,parent:{
            'component':'CollapseTreeRootAIO',
            'subcomponent':'store',
            'aio_ids':aio_ids,
            'parent':parent
        }
        checked = lambda aio_ids:{
            'component':'CollapseTreeRootAIO',
            'subcomponent':'checked',
            'aio_ids':aio_ids
        }

    ids = ids

    def __init__(
      self,data,
      div_props=None,
      aio_id=None,filter=""
    ):
        """CollapseTreeRootAIO is an All-in-One component that is composed
        of a parent `html.Div`.
        - `data` - The data used to create children TreeViewNodeAIO
        - `div_props` - A dictionary of properties passed into the html.Div component.
        - `filter` - String to filter displayed content
        - `aio_id` - The All-in-One component ID used to generate components's dictionary IDs.
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        parent = str(uuid.uuid4())

        
        _div_props = {'children':[components.collapse_tree_node.CollapseTreeNodeAIO(item,with_button=False,className='category2',parent=parent) for item in data]}
        if div_props:
            _div_props.update(div_props)

        super().__init__([
            html.Div(id=self.ids.div(aio_id), **_div_props),
            dcc.Store(id=self.ids.store(aio_id,parent),**{'storage_type':'memory','data':{'filter':filter,'json':data}}),
            dcc.Store(id=self.ids.checked(aio_id),**{'storage_type':'memory','data':{'Yes':[],'No':[],'NA':[]}})
        ])