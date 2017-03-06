package harel.ohad.dronesimulator;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.ArrayMap;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity
{
    enum eDroneStatus
    {
        ON_GROUND,
        AIRBORNE,
        LANDING
    }

    private TextView mStatusLbl;
    private EditText mServerIpEntry;;
    private Button mTakeOffBtn;
    private Button mRTLBtn;
    private Button mLandBtn;
    private Button mFinishLandBtn;
    private int mDroneNum;
    private DroneClient mDroneClient;

    private eDroneStatus mDroneStatus;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        this.init();
    }

    private void init()
    {
        this.mStatusLbl = (TextView) findViewById(R.id.droneStatusLbl);
        this.mServerIpEntry = (EditText) findViewById(R.id.serverIPEntry);
        this.mServerIpEntry.setText(Config.serverIP);
        this.mTakeOffBtn = (Button) findViewById(R.id.takeOffBtn);
        this.mRTLBtn = (Button) findViewById(R.id.rtlBtn);
        this.mLandBtn = (Button) findViewById(R.id.landBtn);
        this.mFinishLandBtn = (Button) findViewById(R.id.landedBtn);
        this.changeDroneStatus(eDroneStatus.ON_GROUND);
        this.mDroneClient = new DroneClient(getApplicationContext());
        this.mDroneClient.execute();
    }

    private void changeDroneStatus(eDroneStatus status)
    {
        this.mDroneStatus = status;
        switch (this.mDroneStatus)
        {
            case ON_GROUND:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.onTheGround));
                this.mTakeOffBtn.setEnabled(true);
                this.mRTLBtn.setEnabled(false);
                this.mLandBtn.setEnabled(false);
                this.mFinishLandBtn.setEnabled(false);
                break;
            }
            case AIRBORNE:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.droneIsAirborne));
                this.mTakeOffBtn.setEnabled(false);
                this.mRTLBtn.setEnabled(true);
                this.mLandBtn.setEnabled(true);
                this.mFinishLandBtn.setEnabled(false);
                break;
            }
            case LANDING:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.droneIsLanding));
                this.mTakeOffBtn.setEnabled(false);
                this.mRTLBtn.setEnabled(false);
                this.mLandBtn.setEnabled(false);
                this.mFinishLandBtn.setEnabled(true);
                break;
            }
        }
    }

    public void onClick_takeOff(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("droneNum", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "takeoff");
        this.mDroneClient.sendMsg(map);
        changeDroneStatus(eDroneStatus.AIRBORNE);
    }

    public void onClick_rtl(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("droneNum", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "rtl");
        this.mDroneClient.sendMsg(map);
        changeDroneStatus(eDroneStatus.LANDING);
    }

    public void onClick_land(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("droneNum", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "land");
        this.mDroneClient.sendMsg(map);
        changeDroneStatus(eDroneStatus.LANDING);
    }

    public void onClick_landed(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("droneNum", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "landFin");
        this.mDroneClient.sendMsg(map);
        changeDroneStatus(eDroneStatus.ON_GROUND);
    }

    public void onClick_subServerIP(View view)
    {
        Config.serverIP = this.mServerIpEntry.getText().toString();
        this.mDroneClient.closeConnection();
        this.mDroneClient = new DroneClient(getApplicationContext());
        this.mDroneClient.execute();
        Toast.makeText(this, "server ip changed", Toast.LENGTH_SHORT).show();
    }

    protected void onDestroy()
    {
        this.mDroneClient.closeConnection();
        try
        {
            Thread.sleep(500);
        }
        catch (InterruptedException e)
        {
            e.printStackTrace();
        }
        super.onDestroy();
    }


}
