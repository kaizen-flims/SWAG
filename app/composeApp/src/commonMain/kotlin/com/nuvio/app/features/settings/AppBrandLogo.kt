package com.nuvio.app.features.settings

import androidx.compose.foundation.Image
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import nuvio.composeapp.generated.resources.Res
import nuvio.composeapp.generated.resources.swag_icon
import org.jetbrains.compose.resources.painterResource

@Composable
internal fun AppBrandLogo(
    modifier: Modifier = Modifier,
    contentDescription: String? = null,
) {
    Image(
        painter = painterResource(Res.drawable.swag_icon),
        contentDescription = contentDescription,
        contentScale = ContentScale.Fit,
        modifier = modifier,
    )
}
