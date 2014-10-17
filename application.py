import os, json, wx, sys

a = wx.App(False)

commandKey = wx.MOD_CMD if sys.platform == 'darwin' else wx.MOD_CONTROL

appName = 'Typing Tutor'
appVersion = '1.0'

if sys.platform == 'darwin':
 from AppKit import NSSearchPathForDirectoriesInDomains
 # http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
 # NSApplicationSupportDirectory = 14
 # NSUserDomainMask = 1
 # True for expanding the tilde into a fully qualified path
 appData = os.path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], appName)
elif sys.platform == 'win32':
 appData = os.path.join(os.environ['APPDATA'], appName)
else:
 appData = path.expanduser(path.join('~', '.%s' % appName))

if not os.path.exists(appData):
 os.mkdir(appData)
    
configFile = os.path.join(appData, 'config.json')
config = dict()
config['volume'] = 100
config['verbose'] = True
config['playSounds'] = True
config['keyboardHelper'] = {
 'a': 'left little finger',
 's': 'left ring finger',
 'd': 'left middle finger',
 'f': 'left index finger',
 'g': 'left index finger',
 'h': 'right index finger',
 'j': 'right index finger',
 'k': 'right middle finger',
 'l': 'right ring finger',
 ';': 'right little finger',
 '\'': 'right little finger',
 'q': 'left little finger',
 'w': 'left ring finger',
 'e': 'left middle finger',
 'r': 'left index finger',
 't': 'left index finger',
 'y': 'right index finger',
 'u': 'right index finger',
 'i': 'right middle finger',
 'o': 'right ring finger',
 'p': 'right little finger',
 '\\': 'left little finger',
 'z': 'left ring finger',
 'x': 'left middle finger',
 'c': 'left index finger',
 'v': 'left index finger',
 'b': 'left or right index finger',
 'n': 'right index finger',
 'm': 'right index finger',
 ',': 'right ring finger',
 '.': 'right little finger',
 '\n': 'right little finger',
 '/': 'right little finger',
 '1': 'left little finger',
 '2': 'left ring finger',
 '3': 'left middle finger',
 '4': 'left index finger',
 '5': 'left index finger',
 '6': 'left index finger',
 '7': 'right index finger',
 '8': 'right middle finger',
 '9': 'right ring finger',
 '0': 'right little finger',
 '[': 'key just to the right of p',
 ']': 'key two to the right of p',
 ' ': 'the long bar across the bottom of the keyboard, pressed with either thumb',
 '`': 'key to the left of 1',
 '-': 'key to the right of 0',
 '=': 'key to the left of backspace',
 ':': 'shift and ;',
 '|': 'shift and \\',
 '~': 'shift and #',
 '#': 'key in the crook of the enter key'
}
if os.path.exists(configFile) and os.path.isfile(configFile):
 with open(configFile, 'r') as f:
  try:
   c = json.loads(f.read())
   for k in c.keys():
    config[k] = c[k]
  except Exception as problem:
   wx.MessageBox(repr(problem), 'Error')
  f.close()
def save():
 with open(configFile, 'w') as f:
  f.write(json.dumps(config, indent = 1))
  f.close()
