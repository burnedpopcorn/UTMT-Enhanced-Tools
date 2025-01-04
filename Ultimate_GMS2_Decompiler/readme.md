# Ultimate_GMS2_Decompiler

The Ultimate GMS2 Decompiler!
(Uses GMS2_Decompiler_FIXED as a Base)

Original Script by loypoll

Major Improvements and Fixes by me

### Ultimate_GMS2_Decompiler Features:
- Enum Declarations are Automatically Extracted and added into the Project, no further action is required
    - (Enum Declaration Feature is only for UA and UTMTCE, because UTMT doesn't use them)
- Asset_Order, a Note within the Project, is available for those that want an absolute PERFECT Decompilation, which can be used to find an Asset's ID, so you can replace any instance of it with the Asset Name
- Added Support for both UTMT and UTMTCE
    - (UTMTCE ONLY) state.throw and state.parry were globally replaced with state.parry_ and state.throw_ as GameMaker would think the Enum Declaration was calling for parry() and throw() functions
- (NEW) Added Ability to Apply TextureGroups to Sprites and Tilesets

These Changes incorperate both
BetterExportGMS2Enums.csx and BetterExportAssetsOrder.csx
making both obsolete

### GMS2_Decompiler_FIXED Changes:
- Start-up Greetings and Credits Pop-Up
- Sprites and TileSets that have no associated image attached to them no longer throw an exception, and will still allow decompilation to finish
- Lists any encountered null sprite/tileset in the error text log

> [!IMPORTANT]
> Download ```Ultimate_GMS2_Decompiler_UA.csx``` for the UnderAnalyzer Version of the Script
>
> Download ```Ultimate_GMS2_Decompiler_UTMT.csx``` for the UTMT Version of the Script
>
> Download ```Ultimate_GMS2_Decompiler_UTMTCE.csx``` for the UTMTCE Version of the Script
>
> Use UTMTCE v0.6 (Latest Github Artifacts)
