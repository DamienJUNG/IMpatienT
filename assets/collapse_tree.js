function nodes_matching_filter(json, filter) {
    const matching = []
    //Si le noeud courant a des enfants
    if (json.children.length > 0) {
        //Pour chaque enfant
        json.children.forEach(item => {
            //On lance une recherche et récupère ceux qu'il correspondent au filtre
            matching.push(...nodes_matching_filter(item, filter))
        })
    }
    //Si le noeud a des enfants qui correspondent au filtre, ou s'il correspond au filtre
    if (matching.length != 0 ||
        json.name.text.toLowerCase().includes(filter))
        //Alors on l'ajoute
        matching.push(json.name.text)
    //On renvoie le tableau de noeuds qui correspondent au filtre
    return matching
}

window.dash_clientside = {
    clientside: {
        update_checked:
            (value, checked, label) => {
                // console.log(label)
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
                //console.log(is_open, n)
                if (n)
                    return [!is_open, is_open == true ? "assets/cross_to_right.jpg" : "assets/cross_to_down.jpg"]
                return [is_open, "assets/cross_to_right.jpg"]
            },
        search_nodes:
            (store, node, style) => {
                if (store.length == 0) return style
                const filter = store[0]['filter']
                const json = store[0]['json']
                const matching = []
                json.forEach(root => {
                    matching.push(...nodes_matching_filter(root, filter.toLowerCase()))
                })
                // console.log(filter)
                // console.log(matching)
                node.map((child, i) => {
                    if (matching.includes(child[0]['props']['children'][2]['props']['label'][0]))
                        style[i] = {}
                    else
                        style[i] = { 'display': 'none' }
                })
                return style
            },
        update_filter:
            (i, input, data) => {
                data[0]['filter'] = input
                return data
            },
        update_selected_rows:
            (checked_box, selected_row_ids) => {
                const triggered = dash_clientside.callback_context.triggered.map(t => t.prop_id)
                console.log(selected_row_ids, "start")
                console.log(triggered, "tri")
                if (triggered.length == 1) {
                    const start = triggered[0].indexOf(":") + 1
                    const end = triggered[0].indexOf(",")
                    const index = parseInt(triggered[0].substring(start, end))
                    console.log("index", index)
                    if (!selected_row_ids.includes(index)) selected_row_ids.push(index)
                    else selected_row_ids = selected_row_ids.filter(i => i != index)
                }
                console.log(selected_row_ids, "end")
                return selected_row_ids
            }
    }
}