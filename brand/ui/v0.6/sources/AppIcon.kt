package io.github.yaossr02.mushroomscout.ui

import androidx.annotation.DrawableRes
import androidx.compose.foundation.layout.size
import androidx.compose.material3.LocalContentColor
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import io.github.yaossr02.mushroomscout.R

/**
 * Every function icon of the app, and the one place a function is given its icon: Phosphor Icons
 * (MIT), the bold weight normally and the filled one when selected ([Icon]'s `selected`). Marks
 * that are actions rather than things (plus, close, check, arrows…) have no filled form: theirs is
 * the bold one again. The drawables are generated from these names by tools/dev/phosphor_icons.py.
 * No emoji or other icon set stands for a function; the mushroom and flower drawings are content.
 */
enum class AppIcon(@DrawableRes val regular: Int, @DrawableRes val fill: Int) {
    // map and its top bar
    Search(R.drawable.ph_magnifying_glass, R.drawable.ph_magnifying_glass_fill),
    Layers(R.drawable.ph_stack, R.drawable.ph_stack_fill),
    Filter(R.drawable.ph_funnel, R.drawable.ph_funnel_fill),
    Settings(R.drawable.ph_gear_six, R.drawable.ph_gear_six_fill),
    Crosshair(R.drawable.ph_crosshair_simple, R.drawable.ph_crosshair_simple_fill),
    Locate(R.drawable.ph_gps_fix, R.drawable.ph_gps_fix_fill),
    FitAll(R.drawable.ph_corners_out, R.drawable.ph_corners_out),
    ZoomIn(R.drawable.ph_plus, R.drawable.ph_plus),
    ZoomOut(R.drawable.ph_minus, R.drawable.ph_minus),
    // the side column
    Auto(R.drawable.ph_robot, R.drawable.ph_robot_fill),
    Tasks(R.drawable.ph_bookmark_simple, R.drawable.ph_bookmark_simple_fill),
    Records(R.drawable.ph_clipboard_text, R.drawable.ph_clipboard_text_fill),
    Scan(R.drawable.ph_scan, R.drawable.ph_scan_fill),
    // the 自動 page's tabs
    Feed(R.drawable.ph_drop, R.drawable.ph_drop_fill),
    Dispatch(R.drawable.ph_compass, R.drawable.ph_compass_fill),
    Lottery(R.drawable.ph_gift, R.drawable.ph_gift_fill),
    // the bottom panel
    Teleport(R.drawable.ph_map_pin, R.drawable.ph_map_pin_fill),
    Route(R.drawable.ph_path, R.drawable.ph_path_fill),
    Reorder(R.drawable.ph_dots_six_vertical, R.drawable.ph_dots_six_vertical),
    List(R.drawable.ph_list_bullets, R.drawable.ph_list_bullets_fill),
    Footprint(R.drawable.ph_footprints, R.drawable.ph_footprints_fill),
    Timezones(R.drawable.ph_globe_hemisphere_east, R.drawable.ph_globe_hemisphere_east_fill),
    Favorite(R.drawable.ph_star, R.drawable.ph_star_fill),
    Recent(R.drawable.ph_clock_counter_clockwise, R.drawable.ph_clock_counter_clockwise_fill),
    // actions
    Add(R.drawable.ph_plus, R.drawable.ph_plus),
    Remove(R.drawable.ph_minus, R.drawable.ph_minus),
    Undo(R.drawable.ph_arrow_counter_clockwise, R.drawable.ph_arrow_counter_clockwise),
    Rotate(R.drawable.ph_arrow_clockwise, R.drawable.ph_arrow_clockwise),
    Play(R.drawable.ph_play, R.drawable.ph_play_fill),
    Pause(R.drawable.ph_pause, R.drawable.ph_pause_fill),
    Stop(R.drawable.ph_stop, R.drawable.ph_stop_fill),
    Copy(R.drawable.ph_copy, R.drawable.ph_copy_fill),
    OpenOutside(R.drawable.ph_arrow_square_out, R.drawable.ph_arrow_square_out_fill),
    Share(R.drawable.ph_share_network, R.drawable.ph_share_network_fill),
    Delete(R.drawable.ph_trash, R.drawable.ph_trash_fill),
    Check(R.drawable.ph_check, R.drawable.ph_check),
    Close(R.drawable.ph_x, R.drawable.ph_x),
    More(R.drawable.ph_dots_three, R.drawable.ph_dots_three),
    SkipForward(R.drawable.ph_skip_forward, R.drawable.ph_skip_forward_fill),
    SkipBack(R.drawable.ph_skip_back, R.drawable.ph_skip_back_fill),
    // the floating button
    FloatMenu(R.drawable.ph_squares_four, R.drawable.ph_squares_four_fill),
    Ticket(R.drawable.ph_ticket, R.drawable.ph_ticket_fill),
    LightSpeed(R.drawable.ph_lightning, R.drawable.ph_lightning_fill),
    Backspace(R.drawable.ph_backspace, R.drawable.ph_backspace_fill),
    ReturnToApp(R.drawable.ph_arrow_u_up_left, R.drawable.ph_arrow_u_up_left),
    // navigation
    Back(R.drawable.ph_arrow_left, R.drawable.ph_arrow_left),
    Previous(R.drawable.ph_caret_left, R.drawable.ph_caret_left),
    Next(R.drawable.ph_caret_right, R.drawable.ph_caret_right),
    Expand(R.drawable.ph_caret_down, R.drawable.ph_caret_down),
    Collapse(R.drawable.ph_caret_up, R.drawable.ph_caret_up),
    // states
    Info(R.drawable.ph_info, R.drawable.ph_info_fill),
    Warning(R.drawable.ph_warning, R.drawable.ph_warning_fill),
}

/** Icon sizes (dp): 16 beside text and in buttons, 18 in bars and chips on the map, 20 on its floating buttons. Separate from the touch area ([TouchTarget]). */
object IconSize {
    val S = 16.dp
    val M = 18.dp
    val L = 20.dp
}

/** The least a tappable thing takes (Android's 48 dp), whatever its icon's size. */
val TouchTarget = 48.dp

/**
 * For the floating panels drawn over Pikmin Bloom (Android views, not Compose): [icon] before this
 * text, in the text's colour, at [size]; alone when the text is empty.
 */
fun android.widget.TextView.setAppIcon(icon: AppIcon, size: Dp = IconSize.S, filled: Boolean = false) {
    val px = (size.value * resources.displayMetrics.density).toInt()
    val d = androidx.core.content.ContextCompat.getDrawable(context, if (filled) icon.fill else icon.regular)!!.mutate()
    d.setBounds(0, 0, px, px)
    d.setTint(currentTextColor)
    setCompoundDrawablesRelative(d, null, null, null)
    compoundDrawablePadding = if (text.isNullOrEmpty()) 0 else px / 4
}

/**
 * [icon] at [size] in [tint]; [selected] draws it filled (the one rule for on / off: filled and
 * the primary colour when on, bold outline when off). [contentDescription] null: decoration
 * beside a text that says it.
 */
@Composable
fun Icon(
    icon: AppIcon,
    contentDescription: String?,
    modifier: Modifier = Modifier,
    size: Dp = IconSize.S,
    selected: Boolean = false,
    tint: Color = LocalContentColor.current,
) {
    androidx.compose.material3.Icon(
        painterResource(if (selected) icon.fill else icon.regular), contentDescription, modifier.size(size), tint = tint,
    )
}
