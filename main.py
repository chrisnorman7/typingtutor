import wx, application, speech, os, random, time, pygame.mixer, webbrowser

pygame.mixer.init(frequency = 44100) # Get the mixer ready for sounds.
class MyTextCtrl(wx.TextCtrl):
 """This class is used so that every time tehe value gets set, the cursor is jumped to the end, instead of the beginning (which is the wx default)."""
 def __init__(self, panel):
  """Set up the class with the provided panel. Fill in all other values automatically."""
  super(MyTextCtrl, self).__init__(panel, style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
 def SetValue(self, value):
  """Set the value as per usual, then move the insertion point to the end."""
  super(MyTextCtrl, self).SetValue(value)
  if self.GetValue():
   self.SetInsertionPoint(len(self.GetValue()) + 1) # Move it 1 past the end (indices start at 0).

class MainFrame(wx.Frame):
 """This is the main window of the program."""
 def __init__(self):
  """Construct the class."""
  # Give the parent class a good seeing too:
  super(MainFrame, self).__init__(None, title = application.appName)
  self.tutorIndex = -1 # One less than the position of the next letter to be spoken by self.startTutoring.
  self.fileContents = '' # The stuff for self.startTutor to run over.
  self.mistakes = 0 # The number of mistakes the user has made.
  self.started = 0 # The time the user started.
  self.finished = False # Has the user finished the current exercise yet?
  self.sounds = dict()
  fileMenu = wx.Menu() # Create the file menu.
  helpMenu = wx.Menu() # Create the help menu.
  self.Bind(wx.EVT_MENU, self.openFile, fileMenu.Append(wx.ID_OPEN, '&Open\tCTRL+O')) # Add open to the file menu, and bind it.
  fileMenu.AppendSeparator() # Put a seperator before quit.
  self.Bind(wx.EVT_MENU, self.quit, fileMenu.Append(wx.ID_EXIT, '&Quit')) # Add a quit item.
  self.Bind(wx.EVT_MENU, self.about, helpMenu.Append(wx.ID_ABOUT, '&About\tF1')) # Add an about item to the help menu and bind.
  menuBar = wx.MenuBar() # Create the main menu bar.
  menuBar.Append(fileMenu, '&File') # Add the file menu to the main menu.
  menuBar.Append(helpMenu, '&Help') # Add the help menu to the main menu.
  self.SetMenuBar(menuBar) # Set the main menu bar.
  p = wx.Panel(self) # There is no tab order without panels.
  mainSizer = wx.BoxSizer(wx.VERTICAL) # Make all the controls the right size and vertically array them.
  self.label = wx.StaticText(p, label = 'F11 for mute, f12 to toggle key descriptions, and tab to repeat the next key')
  mainSizer.Add(self.label, 0, wx.GROW) # Label the entry field.
  self.entry = MyTextCtrl(p)
  mainSizer.Add(self.entry, 1, wx.GROW)
  wx.EVT_CHAR(self.entry, self.processKey)
  self.SetSizerAndFit(mainSizer)
  self.Maximize(True)
  self.Show(True)
  self.Bind(wx.EVT_CLOSE, self.OnClose)
 def getVerbose(self):
  return application.config['verbose']
 def setVerbose(self, value):
  application.config['verbose'] = value
 def getKeyboardHelper(self):
  return application.config['keyboardHelper']
 def setKeyboardHelper(self, value):
   application.config['keyboardHelper'] = value
 def getPlaySounds(self):
  return application.config['playSounds']
 def setPlaySounds(self, value):
  application.config['playSounds'] = value
 def sound(self, sound):
  if self.getPlaySounds():
   if self.sounds.has_key(sound):
    snd = self.sounds[sound]
   else:
    snd = pygame.mixer.Sound(os.path.join('sounds', sound + '.wav'))
    self.sounds[sound] = snd
   snd.set_volume(float(application.config['volume']) / 100)
   snd.play()
   return snd
  else:
   return False
 def getCurrentLetter(self):
  help = ''
  if not self.fileContents:
   l = 'No exercise loaded.'
  elif self.tutorIndex < 0:
   l = 'Press enter to begin.'
  elif self.finished:
   l = 'You have completed this exercise. Use your arrow keys to see your scores.'
  else:
   l = self.fileContents[self.tutorIndex]
   if self.getVerbose() and self.getKeyboardHelper().has_key(l.lower()):
    help = ' (%s)' % self.getKeyboardHelper()[l]
  if l.isupper():
   l = 'capital ' + l.lower()
  elif l == ' ':
   l = 'space'
  elif l == '\n':
   l = 'New line'
  l = l.title() + help
  self.label.SetLabel(l)
  return l
 def processKey(self, event):
  kc, mods = event.GetKeyCode(), event.GetModifiers()
  if kc == wx.WXK_TAB and not mods:
   return speech.speech.output(self.getCurrentLetter())
  elif kc == wx.WXK_F1 and not mods:
   self.about()
  elif kc == wx.WXK_F11:
   if not mods:
    return self.toggleMute()
   elif mods == application.commandKey:
    return self.volumeDown()
  elif kc == wx.WXK_F12:
   if not mods:
    return self.toggleVerbosity()
   elif mods == application.commandKey:
    return self.volumeUp()
  elif kc == wx.WXK_CONTROL_O:
   return self.openFile(event)
  elif kc in [wx.WXK_UP, wx.WXK_DOWN, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_HOME, wx.WXK_END, wx.WXK_F4]:
   pass
  elif self.fileContents:
   if self.tutorIndex < 0 or (kc == ord(self.fileContents[self.tutorIndex]) or (kc == wx.WXK_RETURN and self.fileContents[self.tutorIndex] == '\n')):
    if self.tutorIndex == len(self.fileContents) - 1:
     self.finished = True
     self.sound('finish')
     message = 'You have completed this exercise in %.1f seconds, with %s %s out of %s typed incorrectly.' % ((time.time() - self.started), ('no' if not self.mistakes else self.mistakes), ('letter' if self.mistakes == 1 else 'letters'), len(self.fileContents))
     wx.MessageBox(message, 'Congratulations')
     self.entry.SetValue(message + '\n\n' + self.fileContents)
    else:
     self.startTutor()
   else:
    self.mistakes += 1
    self.sound('wrong')
    speech.speech.output(self.getCurrentLetter())
  event.Skip()
 def openFile(self, event):
  dlg = wx.FileDialog(self, 'Select an exercise', 'exercises', '', '*.txt')
  if dlg.ShowModal() == wx.ID_OK:
   with open(dlg.GetPath(), 'r') as f:
    self.fileContents = f.read()
    self.tutorIndex = -2
    f.close()
    self.startTutor()
  dlg.Destroy()
 def startTutor(self):
  if not self.fileContents:
   wx.MessageBox('No file loaded.', 'error')
  else:
   if self.tutorIndex == -2:
    self.tutorIndex = -1
    self.started = time.time()
    return self.sound(os.path.join('music', random.choice(os.listdir(os.path.join('sounds', 'music'))).strip('.wav')))
   else:
    if not self.tutorIndex:
     self.entry.SetValue('')
    self.tutorIndex += 1
   speech.speech.get_first_available_output().silence()
   speech.speech.output(self.getCurrentLetter())
 def toggleVerbosity(self):
  self.setVerbose(not self.getVerbose())
  if self.fileContents and not self.finished:
   self.getCurrentLetter()
  speech.speech.output('Verbocity set to ' + ('high' if self.getVerbose() else 'low') + '.')
 def toggleMute(self):
  self.setPlaySounds(not self.getPlaySounds())
  speech.speech.output('Sounds ' + ('on' if self.getPlaySounds() else 'off') + '.')
 def OnClose(self, event):
  try:
   application.save()
  except Exception as problem:
   wx.MessageBox(repr(problem), 'Error')
  finally:
   event.Skip()
 def volumeDown(self):
  self.setVolume(application.config['volume'] - 10)
 def volumeUp(self):
  self.setVolume(application.config['volume'] + 10)
 def setVolume(self, volume):
  if volume > 100 or volume < 0:
   if volume > 100:
    volume = 100
   else:
    volume = 0
   wx.Bell()
  application.config['volume'] = int(volume)
  speech.speech.output('Volume set to %s%%.' % application.config['volume'])
  volume = float(volume) / 100
  for s in self.sounds:
   self.sounds[s].set_volume(volume)
 def quit(self, event):
  """Quits the program."""
  self.Close(True)
 def about(self, event):
  """Show an about dialog, and give the user the option to visit the website."""
  def website(event):
   webbrowser.open('http://www.guitarbytouch.com/software/')
   f.Close(True)
  def quit(event):
   f.Close(True)
  f = wx.Frame(None, title = 'About')
  p = wx.Panel(f)
  s = wx.BoxSizer(wx.VERTICAL)
  s.Add(wx.TextCtrl(p, value = '%s, version %s. Written by Chris Norman of Guitar By Touch.\n\nGet the latest source code from github.com/chrisnorman7/typingtutor.git.' % (application.appName, application.appVersion), style = wx.TE_MULTILINE|wx.TE_READONLY), 1, wx.GROW)
  s2 = wx.BoxSizer(wx.HORIZONTAL)
  www = wx.Button(p, label = '&Visit the website')
  s2.Add(www, 0, wx.GROW)
  f.Bind(wx.EVT_BUTTON, website, www)
  ok = wx.Button(p, label = 'OK')
  s2.Add(ok, 0, wx.GROW)
  f.Bind(wx.EVT_BUTTON, quit, ok)
  s.Add(s2, 0, wx.GROW)
  f.SetSizerAndFit(s)
  f.Maximize(True)
  f.Show(True)

if __name__ == '__main__':
 a = wx.App(False)
 m = MainFrame()
 a.MainLoop()
