package com.aarav.timerapp

import android.app.TimePickerDialog
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.NumberPicker
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*
import kotlin.math.min
var total = 0
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val formatter : NumberPicker.Formatter = NumberPicker.Formatter { String.format("%02d",it) }
        hours_pick.maxValue = 24
        hours_pick.minValue = 0
        hours_pick.setFormatter(formatter)
        hours_pick.wrapSelectorWheel = true
        minutes_pick.maxValue = 60
        minutes_pick.minValue = 0
        minutes_pick.setFormatter(formatter)
        minutes_pick.wrapSelectorWheel = true
        seconds_pick.maxValue = 60
        seconds_pick.minValue = 0
        seconds_pick.setFormatter(formatter)
        seconds_pick.wrapSelectorWheel = true
        start_button.setOnClickListener {
            if (seconds_pick.value == 0 && hours_pick.value == 0 && minutes_pick.value == 0){
                Toast.makeText(this, "Set a valid time", Toast.LENGTH_SHORT).show()
            }
            else{
            val hours = hours_pick.value
            val minutes = minutes_pick.value
            val seconds = seconds_pick.value
            total = hours * 360000 + minutes * 60000 + seconds * 1000
            val intent = Intent(this, TimerActivity::class.java)
            startActivity(intent)
            finish()
        }
            }
    }
}
