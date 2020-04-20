import ui
import sqlite3
import russian_keyboard

class VocabTrainer(object):
  def __init__(self):
    #fl = first lanuage
    #sl = second language
    self.fl = 'German'
    self.sl = 'Russian'
    self.font = 'Helvetica'
    self.fontsize = '36'
    self.colorFL = 'black'
    self.colorSL = 'blue'
    self.direction = 3 #1=fl-sl, 2=sl-fl, 3=mixed
    
    self.fonts = ['ArialMT', 'Arial-BoldMT', 'Courier', 'Courier-Bold', 'Helvetica', 'Helvetica-Bold', 'Verdana', 'Verdana-Bold']
    self.fontsizes = ['18', '24', '36', '48', '72']
    self.colors = ['black', 'brown', 'purple', 'red', 'orange', 'pink', 'blue', 'green', 'yellow', 'lightblue', 'lightgreen']
    self.categories = ['<New>']
    
    self.conn = sqlite3.connect('vocab.db')
    self.curs = self.conn.cursor()
    self.curs.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='settings'")
    if self.curs.fetchone() is None:
      self.curs.execute("CREATE TABLE settings (font VARCHAR(40), fontsize VARCHAR(4), colorFL VARCHAR(20), colorSL VARCHAR(20), nameFL VARCHAR(20), nameSL VARCHAR(20))")
      self.conn.commit()
      self.curs.execute("INSERT INTO settings VALUES(?, ?, ?, ?, ?, ?)", (self.font, self.fontsize, self.colorFL, self.colorSL, self.fl, self.sl))
      self.conn.commit()
      self.curs.execute("CREATE TABLE categories (idc INTEGER PRIMARY KEY, category VARCHAR(80))")
      self.conn.commit()
      self.curs.execute("INSERT INTO categories(category) VALUES('Person')")
      self.conn.commit()
      self.curs.execute("INSERT INTO categories(category) VALUES('Essen')")
      self.conn.commit()
      self.curs.execute("CREATE TABLE vocabulary (id INTEGER PRIMARY KEY, wordFL VARCHAR(80), wordSL VARCHAR(80), idc INT, counter INT, learned BOOLEAN)")
      self.conn.commit()
      self.curs.execute("INSERT INTO vocabulary(wordFL, wordSL, idc, counter, learned) VALUES('Ich', 'Я', 1, 0, 0)")
      #0=false, 1=true
      self.conn.commit()
    else:
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
    self.sets = [None, None, None, None]
    
    self.elements = []
    self.view = ui.load_view()
    self.view['bt_import_export'].enabled = False
    self.view.present("fullscreen")
    self.training = self.view['bt_training']
    self.training.action = self.bt_training_action
    self.input = self.view['bt_input']
    self.input.action = self.bt_input_action
    self.settings = self.view['bt_settings']
    self.settings.action = self.bt_settings_action
    self.import_export = self.view['bt_import_export']
    self.import_export.action = self.bt_import_export_action

  def bt_training_action(self, sender):
    self.hide_Main()
    self.make_switch('sw_fl_sl', 30, 30, False, self.sw_fl_sl_action)
    self.make_label('label1', self.fl + ' => ' + self.sl, 90, 30, 400, 31, self.fonts[0], int(self.fontsizes[0]), color='black')
    self.make_switch('sw_sl_fl', 30, 70, False, self.sw_sl_fl_action)
    self.make_label('label2', self.sl + ' => ' + self.fl, 90, 70, 400, 31, self.fonts[0], int(self.fontsizes[0]), color='black')
    self.make_switch('sw_mixed', 30, 110, True, self.sw_mixed_action)
    self.make_label('label3', 'Mixed', 90, 110, 400, 31, self.fonts[0], int(self.fontsizes[0]), color='black')
    self.make_label('label4', 'Category', 30, 170, 80, 31, self.fonts[0], int(self.fontsizes[0]))
    self.categories[0] = '<All>'
    self.make_tableview('tv_category', 110, 170, 500, 200, self.categories, 0, None)
    self.make_button('button1', 'Start', 30, 400, 150, 100, action=self.bt_training_Okay)
    self.make_button('button2', 'Cancel', 190, 400, 150, 100, action=self.bt_Cancel)

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
    cat = self.categories[self.view['tv_category'].selected_row[1]]
    print(cat)
    self.remove_view_x()
    size = ui.measure_string(self.fl, max_width=0, font=(self.font, int(self.fontsize)), alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)
    self.make_label('label1', self.fl, (self.view.width/2)-(size[0]/2), int(self.fontsize), size[0], int(self.fontsize), self.font, int(self.fontsize), color=self.colorFL) #(self.view.height/2)-size[1]
    button = ui.Button()
    button.name = 'bt_first_page'
    button.frame = self.view.frame
    button.action = self.bt_first_page_action
    self.view.add_subview(button)
    self.elements.append('bt_first_page')
    #self.show_Main()
    
  def bt_first_page_action(self, sender):
    self.remove_view_x()
    self.show_second_page()
    
  def show_second_page(self):
    size = ui.measure_string(self.sl, max_width=0, font=(self.font, int(self.fontsize)), alignment=ui.ALIGN_LEFT, line_break_mode=ui.LB_WORD_WRAP)
    height = int(self.fontsize)
    self.make_label('label1', self.sl, (self.view.width/2)-(size[0]/2), height, size[0], int(self.fontsize), self.font, int(self.fontsize), color=self.colorSL) #(self.view.height/2)-size[1]
    self.make_button('button1', 'Learned', 70, height + 100, 300, 150, action=None)
    self.make_button('button2', 'Not Learned', 380, height + 100, 300, 150, action=None)
    self.make_button('button3', 'Main Menu', 70, height + 300, 610, 150, action=self.show_main_menu)
    
  def show_main_menu(self, sender):
    self.remove_view_x()
    self.show_Main()

  def bt_input_action(self, sender):
    self.hide_Main()
    height = int(self.fontsize) + 10
    self.make_label('label1', self.fl, 6, 6, 700, height, self.font, int(self.fontsize), color=self.colorFL)
    self.make_textfield('textfield1', '', 6, 1* (height + 10), 700, height, self.font, int(self.fontsize), color=self.colorFL)
    self.make_label('label2', self.sl, 6, 2* (height + 10), 700, height, self.font, int(self.fontsize), color=self.colorSL)
    self.make_textfield('textfield2', '', 6, 3* (height + 10), 700, height, self.font, int(self.fontsize), color=self.colorSL)
    russian_keyboard.SetTextFieldPad(self.view['textfield2'])
    self.make_label('label2', 'Category', 6, 4* (height + 10), 700, height, self.font, int(self.fontsize))
    self.make_tableview('tv_category', 6, 5* (height + 10), 700, 4*height, self.categories, 1, self.tableview_tapped_category)
    self.make_button('button1', 'Okay', 6, 9* (height + 10), 150, 100, action=self.bt_input_Okay)
    self.make_button('button2', 'Cancel', 164, 9* (height + 10), 150, 100, action=self.bt_Cancel)
    
  def tableview_tapped_category(self, sender):
    if sender._items[sender.selected_row] == '<New>':
      self.make_popup_view()

  def make_popup_view(self):
    self.view_po = ui.View()
    self.view_po.frame = (0,0,400,200)
    self.view_po.name = 'New Category'
    self.view_po.present('popover',popover_location=(self.view.width/2, self.view.height/2))
    textfield = ui.TextField()
    textfield.name = 'tf_new_category'
    textfield.text = ''
    textfield.frame = (0, 0, 400, int(self.fontsize)+10)
    textfield.clear_button_mode = 'always'
    textfield.font = (self.font, int(self.fontsize))
    textfield.text_color = 'black'
    self.view_po.add_subview(textfield)
    button = ui.Button()
    button.name = 'bt_okay_po'
    button.title = 'okay'
    button.frame = (0,int(self.fontsize)+20,150,80)
    button.border_color = 'blue'
    button.border_width = 1.0
    button.corner_radius = 5
    button.action = self.bt_okay_po_action
    self.view_po.add_subview(button)
    button = ui.Button()
    button.name = 'bt_cancel_po'
    button.title = 'cancel'
    button.frame = (160,int(self.fontsize)+20,150,80)
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
    self.remove_view_x()
    self.show_Main()

  def bt_settings_action(self, sender):
    self.sets = [None, None, None, None]
    height = int(self.fontsize) + 10
    self.hide_Main()
    self.make_label('label1', 'Font:', 6, 6, 140, height, self.font, 24)
    self.make_tableview('tv_font', 140, 6, 308, 160, self.fonts, self.fonts.index(self.font), self.tableview_tapped_font)
    self.make_tableview('tv_fontsize', 450, 6, 308, 160, self.fontsizes, self.fontsizes.index(self.fontsize), self.tableview_tapped_fontsize)
    self.make_label('lb_first_lang', self.fl, 140, 180, 308, height, self.font, int(self.fontsize), color=self.colorFL)
    self.make_label('lb_sec_lang', self.sl, 450, 180, 308, height, self.font, int(self.fontsize), color=self.colorSL)
    self.make_label('label4', 'Color:', 6, 190+height, 140, height, self.font, 24)
    self.make_tableview('tv_color_fl', 140, 190+height, 308, 160, self.colors, self.colors.index(self.colorFL), self.tableview_tapped_colorFL)
    self.make_tableview('tv_color_sl', 450, 190+height, 308, 160, self.colors, self.colors.index(self.colorSL), self.tableview_tapped_colorSL)
    self.make_button('button1', 'Okay', 140, 360+height, 308, 100, action=self.bt_settings_Okay)
    self.make_button('button2', 'Cancel', 450, 360+height, 308, 100, action=self.bt_Cancel)

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
    self.remove_view_x()
    self.show_Main()
    
  def bt_import_export_action(self, sender):
    self.hide_Main()
    self.make_label('label1', 'todo', 6, 6, 308, 32)
    self.make_textfield('textfield1', 'textfield1', 6, 46, 308, 32)
    self.make_button('button1', 'Okay', 6, 94, 150, 100, action=self.bt_import_export_Okay)
    self.make_button('button2', 'Cancel', 164, 94, 150, 100, action=self.bt_Cancel)

  def bt_import_export_Okay(self, sender):
    self.remove_view_x()
    self.show_Main()

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
    self.view.add_subview(label)
    self.elements.append(name)

  def make_switch(self, name, x, y, val, action):
    switch = ui.Switch()
    switch.name = name
    switch.frame = (x, y, 51, 31)
    switch.value = val
    switch.action = action
    self.view.add_subview(switch)
    self.elements.append(name)

  def make_textfield(self, name, text, x, y, width, height, font, size, color='black'):
    textfield = ui.TextField()
    textfield.name = name
    textfield.text = text
    textfield.frame = (x, y, width, height)
    textfield.clear_button_mode = 'always'
    textfield.font = (font, size)
    textfield.text_color = color
    self.view.add_subview(textfield)
    self.elements.append(name)

  def make_button(self, name, title, x, y, width, height, action, color='blue', border=1.0, radius=5):
    button = ui.Button()
    button.name = name
    button.title = title
    button.frame = (x, y, width, height)
    button.border_color = color
    button.border_width = border
    button.corner_radius = radius
    button.action = action
    self.view.add_subview(button)
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
    self.view.add_subview(tableview)
    self.elements.append(name)

  def bt_Cancel(self, sender):
    self.remove_view_x()
    self.show_Main()

  def remove_view_x(self):
    for element in self.elements:
      self.view.remove_subview(self.view[element])
    self.elements = []

VocabTrainer()
