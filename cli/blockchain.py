from utils import load_json_from
from utils import memoize


@memoize
def load_deployed():
    c = load_json_from('deployed_contract.json')

