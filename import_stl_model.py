import sys
import os
from stlprintbrowser.model_importer import import_model

if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1]):
    import_model(sys.argv[1])
else:
    print('No model to import. Stopped importer')
