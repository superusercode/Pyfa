type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusRole1"))
