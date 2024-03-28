package com.example.detectioncape;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity{
    Button scrLangsung, scrGambar;

    @Override
    protected void onCreate(Bundle savedIntanceState)
    {
        super.onCreate(savedIntanceState);
        setContentView(R.layout.activity_main);

        scrLangsung = findViewById(R.id.secaraGambarBtn);
        scrGambar = findViewById(R.id.secaraGambarBtn);

        scrLangsung.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(MainActivity.this, LangsungActivity.class));
            }
        });

        scrGambar.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                startActivity(new Intent(MainActivity.this, GambarActivity.class));
            }
        });
    }

}
