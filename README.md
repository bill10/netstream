# netstream
Visualization of streaming network data


Add a node:
{'an': {'id': str, 'label': str, 'x': num, 'y': num, 'size': num, 'type': ...}}  

Add an edge between existing nodes:
{'ae': {'source': node id, 'target': node id}}  

Add an edge with one new node:  
{'aen': {'new': {'id': str, 'label': str, 'x': num, 'y': num, 'size': num, 'type': ...},   
         'old': node id,
         'source': node id, 'target': node id}}  

Add an edge with two new nodes:  
{'aenn': {'source': {'id': str, 'label': str, 'x': num, 'y': num, 'size': num, 'type': ...},   
          'target': {'id': str, 'label': str, 'x': num, 'y': num, 'size': num, 'type': ...}}  
