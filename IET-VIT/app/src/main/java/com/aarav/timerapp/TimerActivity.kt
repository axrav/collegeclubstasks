package com.aarav.timerapp

import android.annotation.SuppressLint
import android.content.Intent
import android.content.IntentSender
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.CountDownTimer
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_timer.*
import java.util.*


class TimerActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_timer)
        val back = Intent(this, MainActivity::class.java)
        startTimer()
        back_button.setOnClickListener {
            startActivity(back)
            finish()
        }
        stop_button.setOnClickListener {
                Toast.makeText(this, "Timer isnt running", Toast.LENGTH_SHORT).show()
            }

        updateCountDownText()
    }
    private fun startTimer(){
        object: CountDownTimer(total.toLong(), 1000){
            override fun onTick(millisUntilFinished: Long) {
                updateCountDownText()
            }
            @SuppressLint("SetTextI18n")
            override fun onFinish() {
                Time_display.text = "Done"
            }
        }.start()
    }
    private fun updateCountDownText(){
        val hour = (total / (1000*60*60)%24)
        val minute = (total / (1000*60)%60)
        val second = (total / 1000) % 60
        val time = String.format(Locale.getDefault(),"%02d:%02d:%02d", hour, minute, second)
        Time_display.text = time
    }
}