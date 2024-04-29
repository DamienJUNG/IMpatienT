from dash import html,dcc,callback,Output,Input,MATCH,State
import uuid

class SliderWithDivAIO(html.Div):
    class ids:
        slider = lambda aio_ids:{
            'component':'SliderWithDivAIO',
            'subcomponent':'slider',
            'aio_ids':aio_ids
        }
        div = lambda aio_ids:{
            'component':'SliderWithDivAIO',
            'subcomponent':'div',
            'aio_ids':aio_ids
        }

    ids = ids

    def __init__(
            self,
            marks,
            slider_props=None,
            div_props=None,
            aio_id=None
    ):
        """SliderWithDivAIO is an All-in-One component that is composed
        of a parent `html.Div` with a `dcc.Slider` to select option ("`slider`") and a
        `html.Div` ("`div`") component as children.
        The div content is determined by the slider value  
        - `slider_props` - A dictionary of properties passed into the dcc.Slider component.
        - `div_props` - A dictionary of properties passed into the html.Div component.
        - `aio_id` - The All-in-One component ID used to generate the slider and div components's dictionary IDs.

        The All-in-One component dictionary IDs are available as
        - SliderWithDivAIO.ids.slider(aio_id)
        - SliderWithDivAIO.ids.div(aio_id)
        """

        if aio_id is None:
            aio_id = str(uuid.uuid4())

        # Merge user-supplied properties into default properties
        _slider_props = {'included':False,'className':"slider",'step':None,'marks':marks}
        if slider_props:
            string=""
            if 'className' in slider_props:
                string='slider ' +slider_props['className']
            _slider_props.update(slider_props)
            _slider_props['className'] = string

        # Merge user-supplied properties into default properties
        div_props = div_props.copy() if div_props else {'className':'slider-text'}

        # Define the component's layout
        super().__init__([ 
            dcc.Slider(id=self.ids.slider(aio_id), **_slider_props),
            html.Div(id=self.ids.div(aio_id), **div_props)
        ])

    # Define this component's stateless pattern-matching callback
    # that will apply to every instance of this component.
    @callback(
        Output(ids.div(MATCH), 'children'),
        Input(ids.slider(MATCH), 'drag_value'),
        State(ids.slider(MATCH),'marks')
    )
    def update_div_text(key,marks):
        if key is not None:
            return marks[str(key)]
        return ""