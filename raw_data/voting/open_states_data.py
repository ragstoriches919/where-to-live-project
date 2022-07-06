import pyopenstates
import cfg

pyopenstates.set_api_key(cfg.API_KEY_OPENSTATES)
print(pyopenstates.get_metadata("CT"))
