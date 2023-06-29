from fastapi import HTTPException
import inflect
from ..utils.hiddenid import int_to_hash
from ..utils.pg import get_db_sync
from ..response import Response
pluralize = inflect.engine().plural

def make_crud_single(app, model):
    name = model.__name__
    
    plural_name = pluralize(name)
    
    model_db_sync = get_db_sync(model) 
    
    @app.post(f"/{plural_name}")
    def create(artist: model):
        rec = model_db_sync.insert(artist)
        return Response(record=rec)

    @app.get(f"/{plural_name}/{{id}}")
    def read(id: str):
        try:
            return Response(record=model_db_sync[id])
        except IndexError:
            raise HTTPException(status_code=404, detail=f"{name} not found")

    @app.put(f"/{plural_name}/{{id}}")
    def update(id: str, artist: model):
        try:
            model_db_sync[id] = artist
            return {"id": id, "artist": artist}
        except IndexError:
            raise HTTPException(status_code=404, detail=f"{name} not found")

    @app.delete(f"/{plural_name}/{{id}}")
    def delete(id: str):
        try:
            artist = model_db_sync[id]
            del model_db_sync[id]
            return {"id": id, "artist": artist}
        except IndexError:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        
    @app.get(f"/schema/{plural_name}")
    def schema():
        try:
            return model.schema()
        except IndexError:
            raise HTTPException(status_code=404, detail=f"Model {model} not found")
        
    if model._Access.List:
        @app.get(f"/{plural_name}")
        def Index():
            try:
                return model_db_sync.__all__()
            except IndexError:
                raise HTTPException(status_code=404, detail=f"Model {model} not found")


def make_crud(app, models):        
    for model in models:
        make_crud_single(app, model)
    