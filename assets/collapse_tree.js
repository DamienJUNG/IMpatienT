function nodes_matching_filter(json, filter, withId) {
    const matching = []
    if (json.children.length > 0) {
        json.children.forEach(item => {
            matching.push(...nodes_matching_filter(item, filter, withId))
        })
    }
    if (matching.length != 0 ||
        json.name.text.toLowerCase().includes(filter) && !withId ||
        json.id != null && json.id.toLowerCase().includes(filter) && withId
    )
        matching.push(withId ? json.id : json.name.text)
    return matching
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_checked:
            (checked, value, label) => {
                //console.log(value, label.filter(x => x[2] != null))
                label = label.filter(x => x[2] != null)
                checked = { 'Yes': [], 'No': [], 'NA': [] }
                value.map((item, i) => {
                    switch (item) {
                        case 0: checked.NA.push(label[i][2]); break
                        case 1: checked.Yes.push(label[i][2]); break
                        case 2: checked.No.push(label[i][2]); break
                    }
                })
                return value
            },
        update_collapse:
            (n, is_open) => {
                if (n)
                    return [!is_open, is_open == true ? "assets/cross_to_right.jpg" : "assets/cross_to_down.jpg"]
                return [is_open, "assets/cross_to_right.jpg"]
            },
        search_nodes:
            (store, node, style) => {
                const filter = store[0]['filter']
                const json = store[0]['json']
                const matching = []
                json.forEach(root => {
                    matching.push(...nodes_matching_filter(root, filter.toLowerCase(), false))
                })
                console.log(filter)
                console.log(matching)
                node.map((child, i) => {
                    if (matching.includes(child[0]['props']['children'][2]['props']['children'][false ? 2 : 0]))
                        style[i] = {}
                    else
                        style[i] = { 'display': 'none' }
                })
                return style
            },
        update_filter:
            (i, input, data) => {
                if (String(input) != String(data['filter'])) data['filter'] = input
                return data
            }
    }
});