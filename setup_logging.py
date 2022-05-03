# Copy to /Applications/Blender.app/Contents/Resources/X.YY/scripts/startup to
# enable logging.

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)-15s %(levelname)8s %(name)s %(message)s')


def register():
    pass
