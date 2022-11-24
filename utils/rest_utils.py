from http import HTTPStatus

def entity_not_found_response(entity_id):
    return "no item found with the given id: " + str(entity_id), HTTPStatus.NOT_FOUND
