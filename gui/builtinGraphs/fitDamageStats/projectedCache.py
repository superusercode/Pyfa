# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================


from gui.builtinGraphs.base import FitDataCache


class ProjectedDataCache(FitDataCache):

    def getProjModData(self, fit):
        try:
            projectedData = self._data[fit.ID]['modules']
        except KeyError:
            # Format of items for both: (boost strength, optimal, falloff, stacking group)
            webMods = []
            tpMods = []
            projectedData = self._data.setdefault(fit.ID, {})['modules'] = (webMods, tpMods)
            for mod in fit.modules:
                if 'remoteWebifierFalloff' in mod.item.effects or 'structureModuleEffectStasisWebifier' in mod.item.effects:
                    webMods.append((mod.getModifiedItemAttr('speedFactor'), mod.maxRange or 0, mod.falloff or 0, 'default'))
                if 'remoteTargetPaintFalloff' in mod.item.effects or 'structureModuleEffectTargetPainter' in mod.item.effects:
                    tpMods.append((mod.getModifiedItemAttr('signatureRadiusBonus'), mod.maxRange or 0, mod.falloff or 0, 'default'))
        return projectedData
