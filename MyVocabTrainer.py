import ui
import sqlite3
import russian_keyboard
import random
import csv
import unicodedata

class MyView(ui.View):
    def __init__(self):
        #main menu
        self.elements = []
        self.menu = 'Main'
        self.name = 'My Vocabulary Trainer'
        self.training = ui.Button()
        self.training.frame = (233, 100, 300, 100)
        self.training.font = ('<system-bold>', 40)
        self.training.tint_color = 'blue'
        self.training.name = 'bt_training'
        self.training.title = 'Training'
        self.add_subview(self.training)
        self.input = ui.Button()
        self.input.frame = (233, 200, 300, 100)
        self.input.font = ('<system-bold>', 40)
        self.input.tint_color = 'blue'
        self.input.name = 'bt_input'
        self.input.title = 'Input'
        self.add_subview(self.input)
        self.settings = ui.Button()
        self.settings.frame = (233, 300, 300, 100)
        self.settings.font = ('<system-bold>', 40)
        self.settings.tint_color = 'blue'
        self.settings.name = 'bt_settings'
        self.settings.title = 'Settings'
        self.add_subview(self.settings)
        self.import_export = ui.Button()
        self.import_export.frame = (233, 400, 300, 100)
        self.import_export.font = ('<system-bold>', 40)
        self.import_export.tint_color = 'blue'
        self.import_export.name = 'bt_import_export'
        self.import_export.title = 'Import/Export'
        #self.import_export.enabled = False
        self.add_subview(self.import_export)
        self.background_color = 'white'

    def hide_Main(self):
        self.training.hidden = True
        self.input.hidden = True
        self.settings.hidden = True
        self.import_export.hidden = True
  
    def show_Main(self):
        self.training.hidden = False
        self.input.hidden = False
        self.settings.hidden = False
        self.import_export.hidden = False

    def layout(self):
        if self.menu == 'Main':
          offsety = (self.height - 475) / 2
          offsetx = (self.width - 300) / 2
          self['bt_training'].x, self['bt_training'].y = offsetx, offsety
          self['bt_input'].x = offsetx
          self['bt_input'].y = offsety + 125
          self['bt_settings'].x = offsetx
          self['bt_settings'].y = offsety + 2 * 125
          self['bt_import_export'].x = offsetx
          self['bt_import_export'].y = offsety + 3 * 125
        elif self.menu == 'TrainingM':
          height = (self.height - 230) / 2 # 170 + 2* 30
          self['tv_category'].frame = (110,170,self.width-125,height)
          self['button1'].frame = (15, height+200, (self.width-45)/2, height)
          self['button2'].frame = ((self.width-45)/2+30, height+200, (self.width-45)/2, height)
        elif self.menu == 'TrainingFP':
          self['bt_first_page'].frame = self.frame
          offsetx = (self.width - self['label1'].width) / 2
          self['label1'].x = offsetx
          if self['label2'] != None:
            offsetx = (self.width - self['label2'].width) / 2
            self['label2'].x = offsetx
        elif self.menu == 'TrainingSP':
          offsetx = (self.width - self['label1'].width) / 2
          self['label1'].x = offsetx
          if self['label2'] != None:
            offsetx = (self.width - self['label2'].width) / 2
            self['label2'].x = offsetx
          y = self['button1'].y
          bt_height = (self.height - y - 90) / 2
          bt_width = (self.width - 45) / 2
          self['button1'].frame = (15, y, bt_width, bt_height)
          self['button2'].frame = (30+bt_width, y, bt_width, bt_height)
          self['button3'].frame = (15, y+60+bt_height, bt_width*2+15, bt_height)
        elif self.menu == 'Input':
          self['textfield1'].width = self.width - 12
          self['textfield2'].width = self.width - 12
          self['tv_category'].width = self.width - 12
          y = self['tv_category'].y
          height = (self.height - y - 60) / 2
          width = (self.width - 18) / 2
          self['tv_category'].height = height
          self['button1'].frame = (6, y+30+height, width, height)
          self['button2'].frame = (12+width, y+30+height, width, height)
        elif self.menu == 'Settings':
          tv_offsetx = 140
          tv_offsety = 6
          tv_width = (self.width - tv_offsetx - 30) / 2
          tv_height = (self.height - self['lb_first_lang'].height - 42) / 3
          bt_width = (self.width - 45) / 2
          self['tv_font'].frame = (tv_offsetx, tv_offsety, tv_width, tv_height)
          self['tv_fontsize'].frame = (tv_offsetx+tv_width+15, tv_offsety, tv_width, tv_height)
          height = self['lb_first_lang'].height
          tv_offsety = tv_offsety + tv_height + 6
          self['label4'].y = tv_offsety
          self['lb_first_lang'].frame = (tv_offsetx, tv_offsety, tv_width, height)
          self['lb_sec_lang'].frame = (tv_offsetx+tv_width+15, tv_offsety, tv_width, height)
          tv_offsety = tv_offsety + height
          self['tv_color_fl'].frame = (tv_offsetx, tv_offsety, tv_width, tv_height)
          self['tv_color_sl'].frame = (tv_offsetx+tv_width+15, tv_offsety, tv_width, tv_height)
          tv_offsety = tv_offsety + tv_height + 15
          self['button1'].frame = (15, tv_offsety, bt_width, tv_height)
          self['button2'].frame = (bt_width+30, tv_offsety, bt_width, tv_height)
          
    def remove_view_x(self):
        for element in self.elements:
          self.remove_subview(self[element])
        self.elements = []
        
    def make_label(self, name, text, x, y, width, height, font, size, color='black'):
        label = ui.Label()
        label.name = name
        label.text = text
        label.frame = (x, y, width, height)
        label.font = (font, size)
        label.text_color = color
        label.border_color = None
        label.border_width = 0
        label.corner_radius = 0
        self.add_subview(label)
        self.elements.append(name)
  
    def make_switch(self, name, x, y, val, action):
        switch = ui.Switch()
        switch.name = name
        switch.frame = (x, y, 51, 31)
        switch.value = val
        switch.action = action
        self.add_subview(switch)
        self.elements.append(name)
  
    def make_textfield(self, name, text, x, y, width, height, font, size, color='black'):
        textfield = ui.TextField()
        textfield.name = name
        textfield.text = text
        textfield.frame = (x, y, width, height)
        textfield.clear_button_mode = 'always'
        textfield.font = (font, size)
        textfield.text_color = color
        self.add_subview(textfield)
        self.elements.append(name)
  
    def make_button(self, name, title, x, y, width, height, action, color='blue', border=1.0, radius=5):
        button = ui.Button()
        button.name = name
        button.title = title
        button.font = ('<system-bold>', 40)
        button.tint_color = 'blue'
        button.frame = (x, y, width, height)
        button.border_color = color
        button.border_width = border
        button.corner_radius = radius
        button.action = action
        self.add_subview(button)
        self.elements.append(name)
      
    def make_tableview(self, name, x, y, width, height, l, selected_row, action, rowheight = 44):
        tableview = ui.TableView()
        tableview.name = name
        tableview.frame = (x, y, width, height)
        tableview.border_color = 'blue'
        tableview.border_width = 1.0
        tableview.corner_radius = 5
        tableview.row_height = rowheight
        tableview.background_color = 'red'
        lst = ui.ListDataSource(l)
        tableview.data_source = lst
        tableview.delegate = lst
        tableview.editing = False
        lst.action = action
        lst.delete_enabled = False
        tableview.selected_row = (0,selected_row)
        self.add_subview(tableview)
        self.elements.append(name)

class VocabTrainer(object):
  def __init__(self):
    #data for first start:
    #fl = first lanuage
    #sl = second language
    self.fl = 'German'
    self.sl = 'Russian'
    self.font = 'Helvetica'
    self.fontsize = '36'
    self.colorFL = 'black'
    self.colorSL = 'blue'
    self.direction = 3 #1=fl-sl, 2=sl-fl, 3=mixed (fl, sl, fl, sl, ...)
    self.next_language = 1 # 1 = fl, 2 = sl
    
    self.fonts = ['ArialMT', 'Arial-BoldMT', 'Courier', 'Courier-Bold', 'Helvetica', 'Helvetica-Bold', 'Verdana', 'Verdana-Bold']
    self.fontsizes = ['18', '24', '36', '48', '72']
    self.colors = ['black', 'brown', 'purple', 'red', 'orange', 'pink', 'blue', 'green', 'yellow', 'lightblue', 'lightgreen']
    self.categories = ['<New>']
    
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    self.curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
    if self.curs.fetchone() is None:
      #create database with basic structure
      self.curs.execute("CREATE TABLE settings (font VARCHAR(40), fontsize VARCHAR(4), colorFL VARCHAR(20), colorSL VARCHAR(20), nameFL VARCHAR(20), nameSL VARCHAR(20))")
      self.conn.commit()
      self.curs.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?)", (self.font, self.fontsize, self.colorFL, self.colorSL, self.fl, self.sl))
      self.conn.commit()
      self.curs.execute("CREATE TABLE categories (idc INTEGER PRIMARY KEY, category VARCHAR(80))")
      self.conn.commit()
      self.curs.execute("INSERT INTO categories(category) VALUES('Personen')")
      self.conn.commit()
      self.curs.execute("INSERT INTO categories(category) VALUES('Essen')")
      self.conn.commit()
      self.curs.execute("CREATE TABLE vocabulary (id INTEGER PRIMARY KEY, wordFL VARCHAR(80), wordSL VARCHAR(80), idc INT, counter INT, learned BOOLEAN)")
      self.conn.commit()
      self.curs.execute("INSERT INTO vocabulary(wordFL, wordSL, idc, counter, learned) VALUES('Ich', 'Я', 1, 0, 0)")
      self.curs.execute("INSERT INTO vocabulary(wordFL, wordSL, idc, counter, learned) VALUES('Pfannkuchen', 'блины', 2, 0, 0)")
      #0=false, 1=true
      self.conn.commit()
    else:
      # read database table settings
      self.curs.execute("SELECT * FROM settings")
      rows = self.curs.fetchone()
      if len(rows) > 5:
        self.font = rows[0]
        self.fontsize = rows[1]
        self.colorFL = rows[2]
        self.colorSL = rows[3]
        self.fl = rows[4]
        self.sl = rows[5]
    self.curs.execute("SELECT category FROM categories")
    rows = self.curs.fetchall()
    for row in rows:
      self.categories.append(row[0])
    self.curs.close()
    self.conn.close()
    # sets (settings) = font, fontsize, fl-color, sl-color
    self.sets = [None, None, None, None]
    self.vocabIds = []
    self.current_vocab = 0
    
    self.view = MyView()
    self.view.training.action = self.bt_training_action
    self.view.input.action = self.bt_input_action
    self.view.settings.action = self.bt_settings_action
    self.view.import_export.action = self.bt_import_export_action
    self.view.present("fullscreen")

  def bt_training_action(self, sender):
    self.view.hide_Main()
    self.view.make_label('label0', 'Order', 15, 30, 80, 31, self.fonts[1], int(self.fontsizes[0]))
    self.view.make_switch('sw_fl_sl', 110, 30, False, self.sw_fl_sl_action)
    self.view.make_label('label1', self.fl + ' => ' + self.sl, 170, 30, 400, 31, self.fonts[0], int(self.fontsizes[0]), color='black')
    self.view.make_switch('sw_sl_fl', 110, 70, False, self.sw_sl_fl_action)
    self.view.make_label('label2', self.sl + ' => ' + self.fl, 170, 70, 400, 31, self.fonts[0], int(self.fontsizes[0]), color='black')
    self.view.make_switch('sw_mixed', 110, 110, True, self.sw_mixed_action)
    self.view.make_label('label3', 'Mixed', 170, 110, 400, 31, self.fonts[0], int(self.fontsizes[0]), color='black')
    self.view.make_label('label4', 'Category', 15, 170, 80, 31, self.fonts[1], int(self.fontsizes[0]))
    self.categories[0] = '<All>'
    self.view.make_tableview('tv_category', 110, 170, 500, 200, self.categories, 0, None)
    self.view.make_button('button1', 'Start', 30, 400, 150, 100, action=self.bt_training_Okay)
    self.view.make_button('button2', 'Cancel', 190, 400, 150, 100, action=self.bt_Cancel)
    self.view.menu = 'TrainingM'
    #self.view.layout()

  def sw_fl_sl_action(self, sender):
    if sender.value == True:
      if self.view['sw_sl_fl'].value == True:
        self.view['sw_sl_fl'].value = False
      if self.view['sw_mixed'].value == True:
        self.view['sw_mixed'].value = False
      self.direction = 1
    else:
      if self.view['sw_sl_fl'].value == False and self.view['sw_mixed'].value == False:
        self.view['sw_mixed'].value = True
        self.direction = 3
        
  def sw_sl_fl_action(self, sender):
    if sender.value == True:
      if self.view['sw_fl_sl'].value == True:
        self.view['sw_fl_sl'].value = False
      if self.view['sw_mixed'].value == True:
        self.view['sw_mixed'].value = False
      self.direction = 2
    else:
      if self.view['sw_fl_sl'].value == False and self.view['sw_mixed'].value == False:
        self.view['sw_mixed'].value = True
        self.direction = 3
        
  def sw_mixed_action(self, sender):
    if sender.value == True:
      if self.view['sw_sl_fl'].value == True:
        self.view['sw_sl_fl'].value = False
      if self.view['sw_fl_sl'].value == True:
        self.view['sw_fl_sl'].value = False
      self.direction = 3
    else:
      if self.view['sw_sl_fl'].value == False and self.view['sw_fl_sl'].value == False:
        self.view['sw_mixed'].value = True
        self.direction = 3

  def bt_training_Okay(self, sender):
    '''
    1. filter category and not learned words
    2. sort to the smallest count, max 100 words and randomize
    3. which direction // mixed => fl, sl, fl, sl, ...
    '''
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    cat = self.categories[self.view['tv_category'].selected_row[1]]
    self.vocabIds = []
    if cat == '<All>':
      self.curs.execute("SELECT id FROM vocabulary WHERE learned=0 ORDER BY counter LIMIT 100")
      rows = self.curs.fetchall()
    else:
      #todo join
      self.curs.execute("SELECT idc FROM categories WHERE category=(?)",(cat,))
      idc = self.curs.fetchone()[0]
      self.curs.execute("SELECT * FROM vocabulary WHERE learned=0 AND idc=(?) ORDER BY counter LIMIT 100",(idc,))
      rows = self.curs.fetchall()
    for row in rows:
      self.vocabIds.append(row[0])
    random.shuffle(self.vocabIds)
    self.current_vocab = self.vocabIds.pop(0)
    if self.direction == 2:
      self.next_language = 1
      self.curs.execute("SELECT wordSL FROM vocabulary WHERE id=(?)", (self.current_vocab,))
      word = self.curs.fetchone()[0]
      color = self.colorSL
    else:
      self.next_language = 2
      self.curs.execute("SELECT wordFL FROM vocabulary WHERE id=(?)", (self.current_vocab,))
      word = self.curs.fetchone()[0]
      color = self.colorFL
    self.curs.close()
    self.conn.close()
    self.view.remove_view_x()
    self.show_Vocab(word, color)
    button = ui.Button()
    button.name = 'bt_first_page'
    button.frame = self.view.frame
    button.action = self.bt_first_page_action
    self.view.add_subview(button)
    self.view.elements.append('bt_first_page')
    self.view.menu = 'TrainingFP'
    
  def show_Vocab(self, word, color):
    if word.find("(") > 0:
      line1 = word[0:word.find("(")-1]
      line2 = word[word.find("("):]
      size1 = ui.measure_string(line1, max_width=0, font=(self.font, int(self.fontsize)), alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)
      self.view.make_label('label1', line1, 15, int(self.fontsize), size1[0], int(self.fontsize), self.font, int(self.fontsize), color=color)
      size2 = ui.measure_string(line2, max_width=0, font=(self.font, int(self.fontsize)), alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)
      self.view.make_label('label2', line2, 15, int(self.fontsize)*3, size2[0], int(self.fontsize), self.font, int(self.fontsize), color=color)
    else:
      size = ui.measure_string(word, max_width=0, font=(self.font, int(self.fontsize)), alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)
      self.view.make_label('label1', word, 15, int(self.fontsize), size[0], int(self.fontsize), self.font, int(self.fontsize), color=color)
    
  def bt_first_page_action(self, sender):
    self.view.remove_view_x()
    self.show_second_page()
    
  def show_second_page(self):
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    if self.next_language == 2:
      self.curs.execute("SELECT wordSL FROM vocabulary WHERE id=(?)", (self.current_vocab,))
      word = self.curs.fetchone()[0]
      color = self.colorSL
    else:
      self.curs.execute("SELECT wordFL FROM vocabulary WHERE id=(?)", (self.current_vocab,))
      word = self.curs.fetchone()[0]
      color = self.colorFL
    self.curs.close()
    self.conn.close()
    if self.direction != 3:  # swap language if 1 or 2
      if self.next_language == 1:
        self.next_language = 2
      else:
        self.next_language = 1
    self.show_Vocab(word, color)
    height = int(self.fontsize) * 5
    self.view.make_button('button1', 'Learned', 70, height, 300, 150, action=self.bt_learned)
    self.view.make_button('button2', 'Not Learned', 380, height, 300, 150, action=self.bt_not_learned)
    self.view.make_button('button3', 'Main Menu', 70, height + 200, 610, 150, action=self.show_main_menu)
    self.view.menu = 'TrainingSP'
    
  def bt_learned(self, sender):
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    self.curs.execute("UPDATE vocabulary SET learned=1 WHERE id=(?)", (self.current_vocab,))
    self.conn.commit()
    self.curs.close()
    self.conn.close()
    if len(self.vocabIds) > 0:
      self.remove_view_x()
      self.show_training_loop()
    else:
      self.remove_view_x()
      self.view.menu = 'Main'
      self.view.show_Main()
    
  def bt_not_learned(self, sender):
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    self.curs.execute("SELECT counter FROM vocabulary WHERE id=(?)", (self.current_vocab,))
    counter = int(self.curs.fetchone()[0])
    counter += 1
    self.curs.execute("UPDATE vocabulary SET counter=(?) WHERE id=(?)", (counter, self.current_vocab))
    self.conn.commit()
    self.curs.close()
    self.conn.close()
    if len(self.vocabIds) > 0:
      self.view.remove_view_x()
      self.show_training_loop()
    else:
      self.view.remove_view_x()
      self.view.menu = 'Main'
      self.view.show_Main()
      
  def show_training_loop(self):
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    self.current_vocab = self.vocabIds.pop(0)
    if self.next_language == 2:
      self.curs.execute("SELECT wordSL FROM vocabulary WHERE id=(?)", (self.current_vocab,))
      word = self.curs.fetchone()[0]
      color = self.colorSL
    else:
      self.curs.execute("SELECT wordFL FROM vocabulary WHERE id=(?)", (self.current_vocab,))
      word = self.curs.fetchone()[0]
      color = self.colorFL
    self.curs.close()
    self.conn.close()
    if self.next_language == 1:
      self.next_language = 2
    else:
      self.next_language = 1
    self.show_Vocab(word, color)
    button = ui.Button()
    button.name = 'bt_first_page'
    button.frame = self.view.frame
    button.action = self.bt_first_page_action
    self.view.add_subview(button)
    self.view.elements.append('bt_first_page')
    self.view.menu = 'TrainingFP'
    
  def show_main_menu(self, sender):
    self.view.remove_view_x()
    self.view.menu = 'Main'
    self.view.show_Main()

  def bt_input_action(self, sender):
    self.view.hide_Main()
    self.categories[0] = '<New>'
    height = int(self.fontsize) + 10
    self.view.make_label('label1', self.fl, 6, 6, 700, height, self.font, int(self.fontsize), color=self.colorFL)
    self.view.make_textfield('textfield1', '', 6, 1* (height + 10), 700, height, self.font, int(self.fontsize), color=self.colorFL)
    self.view.make_label('label2', self.sl, 6, 2* (height + 10), 700, height, self.font, int(self.fontsize), color=self.colorSL)
    self.view.make_textfield('textfield2', '', 6, 3* (height + 10), 700, height, self.font, int(self.fontsize), color=self.colorSL)
    russian_keyboard.SetTextFieldPad(self.view['textfield2'])
    self.view.make_label('label2', 'Category', 6, 4* (height + 10), 700, height, self.font, int(self.fontsize))
    self.view.make_tableview('tv_category', 6, 5* (height + 10), 700, 4*height, self.categories, 1, self.tableview_tapped_category)
    self.view.make_button('button1', 'Okay', 6, 9* (height + 10), 150, 100, action=self.bt_input_Okay)
    self.view.make_button('button2', 'Cancel', 164, 9* (height + 10), 150, 100, action=self.bt_Cancel)
    self.view.menu = 'Input'
    
  def tableview_tapped_category(self, sender):
    if sender._items[sender.selected_row] == '<New>':
      self.make_popup_view()

  def make_popup_view(self):
    self.view_po = ui.View()
    self.view_po.frame = (0,0,400,int(self.fontsize)*4)
    self.view_po.name = 'New Category'
    self.view_po.present('popover',popover_location=(self.view.width/2, self.view.height/2))
    textfield = ui.TextField()
    textfield.name = 'tf_new_category'
    textfield.text = ''
    textfield.frame = (6, 6, 388, int(self.fontsize)+10)
    textfield.clear_button_mode = 'always'
    textfield.font = (self.font, int(self.fontsize))
    textfield.text_color = 'black'
    self.view_po.add_subview(textfield)
    y = int(self.fontsize) + 22
    height = self.view_po.height - y - 6
    width = (400 - 18) / 2
    button = ui.Button()
    button.name = 'bt_okay_po'
    button.title = 'Okay'
    button.font = ('<system-bold>', 40)
    button.tint_color = 'blue'
    button.frame = (6,y,width,height)
    button.border_color = 'blue'
    button.border_width = 1.0
    button.corner_radius = 5
    button.action = self.bt_okay_po_action
    self.view_po.add_subview(button)
    button = ui.Button()
    button.name = 'bt_cancel_po'
    button.title = 'Cancel'
    button.font = ('<system-bold>', 40)
    button.tint_color = 'blue'
    button.frame = (12+width,y,width,height)
    button.border_color = 'blue'
    button.border_width = 1.0
    button.corner_radius = 5
    button.action = self.bt_cancel_po_action
    self.view_po.add_subview(button)
    
  def bt_okay_po_action(self, sender):
    if self.view_po['tf_new_category'].text != '':
      self.categories.append(self.view_po['tf_new_category'].text)
    lst = ui.ListDataSource(self.categories)
    self.view['tv_category'].data_source = lst
    self.view['tv_category'].delegate = lst
    lst.action = self.tableview_tapped_category
    self.view['tv_category'].reload()
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    self.curs.execute("INSERT INTO categories(category) VALUES(?)",(self.view_po['tf_new_category'].text,))
    self.conn.commit()
    self.curs.close()
    self.conn.close()
    self.view_po.close()
    
  def bt_cancel_po_action(self, sender):
    self.view_po.close()
    
  def bt_input_Okay(self, sender):
    if self.view['textfield1'].text != '' and self.view['textfield2'].text != '':
      self.conn = sqlite3.connect('vocab.db')
      self.curs = self.conn.cursor()
      self.curs.execute("SELECT idc FROM categories WHERE category=?",(self.categories[self.view['tv_category'].selected_row[1]],))
      idc = self.curs.fetchone()
      self.curs.execute("INSERT INTO vocabulary(wordFL, wordSL, idc, counter, learned) VALUES(?, ?, ?, ?, ?)", (self.view['textfield1'].text, self.view['textfield2'].text, idc[0], 0, 0))
      self.conn.commit()
      self.curs.close()
      self.conn.close()
    self.view.remove_view_x()
    self.view.menu = 'Main'
    self.view.show_Main()

  def bt_settings_action(self, sender):
    self.sets = [None, None, None, None]
    height = int(self.fontsize) + 10
    self.view.hide_Main()
    self.view.make_label('label1', 'Font', 15, 6, 110, height, self.fonts[1], int(self.fontsizes[1]))
    self.view.make_tableview('tv_font', 140, 6, 308, 160, self.fonts, self.fonts.index(self.font), self.tableview_tapped_font)
    self.view.make_tableview('tv_fontsize', 450, 6, 308, 160, self.fontsizes, self.fontsizes.index(self.fontsize), self.tableview_tapped_fontsize)
    self.view.make_label('lb_first_lang', self.fl, 140, 180, 308, height, self.font, int(self.fontsize), color=self.colorFL)
    self.view.make_label('lb_sec_lang', self.sl, 450, 180, 308, height, self.font, int(self.fontsize), color=self.colorSL)
    self.view.make_label('label4', 'Color', 15, 180, 110, height, self.fonts[1], int(self.fontsizes[1]))
    self.view.make_tableview('tv_color_fl', 140, 190+height, 308, 160, self.colors, self.colors.index(self.colorFL), self.tableview_tapped_colorFL)
    self.view.make_tableview('tv_color_sl', 450, 190+height, 308, 160, self.colors, self.colors.index(self.colorSL), self.tableview_tapped_colorSL)
    self.view.make_button('button1', 'Okay', 140, 360+height, 308, 100, action=self.bt_settings_Okay)
    self.view.make_button('button2', 'Cancel', 450, 360+height, 308, 100, action=self.bt_Cancel)
    self.view.menu = 'Settings'

  def tableview_tapped_font(self, sender):
    self.sets[0] = sender._items[sender.selected_row]
    if self.sets[1] is not None:
      self.view['lb_first_lang'].font = (self.sets[0], int(self.sets[1]))
      self.view['lb_sec_lang'].font = (self.sets[0], int(self.sets[1]))
    else:
      self.view['lb_first_lang'].font = (self.sets[0], int(self.fontsize))
      self.view['lb_sec_lang'].font = (self.sets[0], int(self.fontsize))
    if self.sets[2] is not None:
      self.view['lb_first_lang'].text_color = self.sets[2]
    if self.sets[3] is not None:
      self.view['lb_sec_lang'].text_color = self.sets[3]
    self.view.set_needs_display()
    
  def tableview_tapped_fontsize(self, sender):
    self.sets[1] = sender._items[sender.selected_row]
    if self.sets[0] is not None:
      self.view['lb_first_lang'].font = (self.sets[0], int(self.sets[1]))
      self.view['lb_sec_lang'].font = (self.sets[0], int(self.sets[1]))
    else:
      self.view['lb_first_lang'].font = (self.font, int(self.sets[1]))
      self.view['lb_sec_lang'].font = (self.font, int(self.sets[1]))
    if self.sets[2] is not None:
      self.view['lb_first_lang'].text_color = self.sets[2]
    if self.sets[3] is not None:
      self.view['lb_sec_lang'].text_color = self.sets[3]
    self.view.set_needs_display()
    
  def tableview_tapped_colorFL(self, sender):
    self.sets[2] = sender._items[sender.selected_row]
    if self.sets[0] is not None and self.sets[1] is not None:
      self.view['lb_first_lang'].font = (self.sets[0], int(self.sets[1]))
      self.view['lb_sec_lang'].font = (self.sets[0], int(self.sets[1]))
    elif self.sets[0] is not None:
      self.view['lb_first_lang'].font = (self.sets[0], int(self.fontsize))
      self.view['lb_sec_lang'].font = (self.sets[0], int(self.fontsize))
    elif self.sets[1] is not None:
      self.view['lb_first_lang'].font = (self.font, int(self.sets[1]))
      self.view['lb_sec_lang'].font = (self.font, int(self.sets[1]))
    if self.sets[2] is not None:
      self.view['lb_first_lang'].text_color = self.sets[2]
    if self.sets[3] is not None:
      self.view['lb_sec_lang'].text_color = self.sets[3]
    self.view.set_needs_display()

  def tableview_tapped_colorSL(self, sender):
    self.sets[3] = sender._items[sender.selected_row]
    if self.sets[0] is not None and self.sets[1] is not None:
      self.view['lb_first_lang'].font = (self.sets[0], int(self.sets[1]))
      self.view['lb_sec_lang'].font = (self.sets[0], int(self.sets[1]))
    elif self.sets[0] is not None:
      self.view['lb_first_lang'].font = (self.sets[0], int(self.fontsize))
      self.view['lb_sec_lang'].font = (self.sets[0], int(self.fontsize))
    elif self.sets[1] is not None:
      self.view['lb_first_lang'].font = (self.font, int(self.sets[1]))
      self.view['lb_sec_lang'].font = (self.font, int(self.sets[1]))
    if self.sets[2] is not None:
      self.view['lb_first_lang'].text_color = self.sets[2]
    if self.sets[3] is not None:
      self.view['lb_sec_lang'].text_color = self.sets[3]
    self.view.set_needs_display()
    
  def bt_settings_Okay(self, sender):
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    for i in range(0, 4):
      if self.sets[i] is not None:
        if i == 0:
          self.curs.execute("UPDATE settings SET font=? WHERE nameFL=? AND nameSL=?", (self.sets[0], self.fl, self.sl))
          self.conn.commit()
          self.font = self.sets[0]
        elif i == 1:
          self.curs.execute("UPDATE settings SET fontsize=? WHERE nameFL=? AND nameSL=?", (self.sets[1], self.fl, self.sl))
          self.conn.commit()
          self.fontsize = self.sets[1]
        elif i == 2:
          self.curs.execute("UPDATE settings SET colorFL=? WHERE nameFL=? AND nameSL=?", (self.sets[2], self.fl, self.sl))
          self.conn.commit()
          self.colorFL = self.sets[2]
        elif i == 3:
          self.curs.execute("UPDATE settings SET colorSL=? WHERE nameFL=? AND nameSL=?", (self.sets[3], self.fl, self.sl))
          self.conn.commit()
          self.colorSL = self.sets[3]
    self.curs.close()
    self.conn.close()
    self.view.remove_view_x()
    self.view.menu = 'Main'
    self.view.show_Main()
    
  def bt_import_export_action(self, sender):
    self.view.hide_Main()
    self.view.make_label('label1', 'Export:', 6, 6, 308, 32, self.fonts[1], int(self.fontsizes[1]))
    self.view.make_textfield('textfield1', 'test.csv', 6, 46, 308, 32, self.fonts[1], int(self.fontsizes[1]))
    self.view.make_button('button1', 'Okay', 6, 94, 150, 100, action=self.bt_import_export_Okay)
    self.view.make_button('button2', 'Cancel', 164, 94, 150, 100, action=self.bt_Cancel)

  def bt_import_export_Okay(self, sender):
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    self.curs.execute("SELECT * FROM vocabulary")
    vocab = self.curs.fetchall()
    self.curs.close()
    self.conn.close()
    writer = csv.writer(open(self.view['textfield1'].text, "w", encoding='utf-8'), quoting=csv.QUOTE_NONNUMERIC)
    writer.writerows(vocab)
    self.view.remove_view_x()
    self.view.menu = 'Main'
    self.view.show_Main()

  def bt_Cancel(self, sender):
    self.view.remove_view_x()
    self.view.menu = 'Main'
    self.view.show_Main()

VocabTrainer()
