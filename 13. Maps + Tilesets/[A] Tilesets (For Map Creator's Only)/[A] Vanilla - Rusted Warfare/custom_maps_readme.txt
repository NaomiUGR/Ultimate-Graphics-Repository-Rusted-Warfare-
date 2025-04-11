Layers:

'set': completely ignored by the game only used by Tiled for automapping (you should draw on this layer instead of ground)
'Triggers': set map settings, players stats, and create events
'Units': setup starting units, anything else on this layer is ignored
'Items': resource pools must go on this layer to work, trees and other items can appear on this layer. Do not use this layer for map tiles (as pathing may not work).
'Ground': map tiles go on this layer. But do not edit this layer if you are using automapping, as they will get overridden.
