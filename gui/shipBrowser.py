import wx
import controller
import bitmapLoader
import gui.mainFrame

class ShipBrowser(wx.Panel):
    def __init__(self, parent):
        self.built = False
        wx.Panel.__init__(self, parent)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(vbox)

        self.shipMenu = ShipMenu(self)
        vbox.Add(self.shipMenu, 0, wx.EXPAND)

        self.shipView = ShipView(self)
        vbox.Add(self.shipView, 1, wx.EXPAND)

        self.shipImageList = wx.ImageList(16, 16)
        self.shipView.SetImageList(self.shipImageList)

        self.shipRoot = self.shipView.AddRoot("Ships")

        self.raceImageIds = {}
        self.races = ["amarr", "caldari", "gallente", "minmatar", "ore", "serpentis", "angel", "blood", "sansha", "guristas"]
        for race in self.races:
            imageId = self.shipImageList.Add(bitmapLoader.getBitmap("race_%s_small" % race, "icons"))
            self.raceImageIds[race] = imageId

        self.races.append("None")
        #Bind our lookup method to when the tree gets expanded
        self.shipView.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.expandLookup)
        self.idRaceMap = {}
        self.shipView.races = self.races
        self.shipView.idRaceMap = self.idRaceMap

    def build(self):
        if not self.built:
            self.built = True
            cMarket = controller.Market.getInstance()
            shipRoot = cMarket.getShipRoot()
            iconId = self.shipImageList.Add(bitmapLoader.getBitmap("ship_small", "icons"))
            for id, name in shipRoot:
                childId = self.shipView.AppendItem(self.shipRoot, name, iconId, data=wx.TreeItemData(id))
                self.shipView.AppendItem(childId, "dummy")

        self.shipView.SortChildren(self.shipRoot)
    def expandLookup(self, event):
        root = event.Item
        child, cookie = self.shipView.GetFirstChild(root)
        self.idRaceMap.clear()
        if self.shipView.GetItemText(child) == "dummy":
            self.shipView.Delete(child)

            cMarket = controller.Market.getInstance()

            for id, name, race in cMarket.getShipList(self.shipView.GetPyData(root)):
                iconId = self.raceImageIds[race] if race in self.raceImageIds else -1
                self.idRaceMap[id] = race
                self.shipView.AppendItem(root, name, iconId, data=wx.TreeItemData(id))

            self.shipView.SortChildren(root)

class ShipView(wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent)
        treeStyle = self.GetWindowStyleFlag()
        treeStyle |= wx.TR_HIDE_ROOT
        self.SetWindowStyleFlag(treeStyle)

    def OnCompareItems(self, treeId1, treeId2):
        child, cookie = self.GetFirstChild(treeId1)
        if child.IsOk():
            return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))
        else:
            id1 = self.GetPyData(treeId1)
            id2 = self.GetPyData(treeId2)
            c = cmp(self.races.index(self.idRaceMap[id1] or "None"), self.races.index(self.idRaceMap[id2] or "None"))
            if c != 0:
                return c
            else:
                return cmp(self.GetItemText(treeId1), self.GetItemText(treeId2))

class ShipMenu(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)

        for name, art in (("new", wx.ART_NEW), ("rename", wx.ART_FIND_AND_REPLACE), ("copy", wx.ART_COPY), ("delete", wx.ART_DELETE)):
            btn = wx.BitmapButton(self, wx.ID_ANY, wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON))
            setattr(self, name, btn)
            btn.Enable(False)
            btn.SetToolTipString("%s fit." % name.capitalize())
            sizer.Add(btn)
