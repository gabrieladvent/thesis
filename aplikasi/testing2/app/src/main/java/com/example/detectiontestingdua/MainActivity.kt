package com.example.detectiontestingdua

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.provider.MediaStore
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.example.detectiontestingdua.ui.theme.DetectionTestingDuaTheme
import androidx.compose.runtime.*
import androidx.core.app.ActivityCompat
import android.Manifest
import android.content.pm.PackageManager
import android.widget.Toast


@Suppress("DEPRECATION")
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            DetectionTestingDuaTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    DetecApp(activity = this@MainActivity)
                }
            }
        }
    }
    @Deprecated("Deprecated in Java")
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        when (requestCode) {
            1 -> {
                if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                    startActivity(intent)
                } else {
                    Toast.makeText(this, "Izin kamera tidak diberikan", Toast.LENGTH_SHORT).show()
                }
                return
            }
        }
    }

    @Deprecated("Deprecated in Java")
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == 2 && resultCode == RESULT_OK) {
            // Handle selected image here
            data?.data
            // Use the selectedImageUri to do something with the image
        }
    }

}

@Composable
fun DetecApp(activity: Activity){
    ImageShow(
        modifier = Modifier
            .fillMaxSize()
            .wrapContentSize(Alignment.Center)
            .padding(16.dp),
        activity = activity
    )
}

@Composable
fun ImageShow(modifier: Modifier = Modifier, activity: Activity) {
    val isPermissionGranted by remember { mutableStateOf(false) }

    Column(
        modifier = modifier,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
//        Text(
//            text = "DETECTION OBJEK WITH YOLO",
//            style = TextStyle(color = Color.White),
//            modifier = Modifier.padding(8.dp)
//        )
        Image(
            painter = painterResource(id = R.drawable._686385),
            contentDescription = null,
            modifier = Modifier
                .size(300.dp)
                .padding(8.dp)
        )
        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = { /* Aksi yang dijalankan saat tombol Realtime ditekan */ },
            modifier = Modifier.width(300.dp)
        ) {
            Text("Realtime")
        }
        Spacer(modifier = Modifier.height(8.dp)) // Spasi antara tombol

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            Button(
                onClick = {
                    if (!isPermissionGranted) {
                        ActivityCompat.requestPermissions(
                            activity,
                            arrayOf(Manifest.permission.CAMERA),
                            1
                        )
                    } else {
                        val intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                        activity.startActivity(intent)
                    }
                },
            ) {
                Text("Open Camera")
            }
            Button(
                onClick = {
                    val intent = Intent(Intent.ACTION_GET_CONTENT)
                    intent.type = "image/*"
                    activity.startActivity(intent)
                },
            ) {
                Text("Upload Image")
            }
        }
        Spacer(modifier = Modifier.height(8.dp)) // Spasi antara tombol

        Button(
            onClick = { /* Aksi yang dijalankan saat tombol Open Camera ditekan */ },
            modifier = Modifier.width(300.dp)
        ) {
            Text("Petunjuk Penggunaan")
        }
    }
}
