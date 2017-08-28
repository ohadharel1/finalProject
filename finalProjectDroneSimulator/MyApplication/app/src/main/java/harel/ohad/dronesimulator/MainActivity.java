package harel.ohad.dronesimulator;

import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.util.ArrayMap;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;

public class MainActivity extends AppCompatActivity
{
    enum eDroneStatus
    {
        NOT_CONNECTED,
        ON_GROUND,
        AIRBORNE,
        LANDING,
        ERROR
    }

    private final static int shortDelay = 5 * 1000; //5 seconds
    private final static int longDelay = 20 * 1000; //20 seconds
    private final static String LOG_FOLDER = Environment.getExternalStorageDirectory() + "/drone_logs/";
    private final static String LOG_PROXY_NAME = "proxy.log";
    private final static String LOG_TRACKER_NAME = "tracker.log";

    private static MainActivity instance;
    private TextView mStatusLbl;
    private EditText mServerIpEntry;;
    private Button mTakeOffBtn;
    private Button mRTLBtn;
    private Button mLandBtn;
    private Button mGoUpBtn;
    private Button mGoDownBtn;
    private Button mGoFWDBtn;
    private Button mGoBackBtn;
    private Button mMissionBtn;
    private Spinner mErrorSpinner;

    private int mDroneNum;
    private int mErrorID;
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
        instance = this;
        this.mStatusLbl = (TextView) findViewById(R.id.droneStatusLbl);
        this.mServerIpEntry = (EditText) findViewById(R.id.serverIPEntry);
        this.mServerIpEntry.setText(Config.serverIP);
        this.mTakeOffBtn = (Button) findViewById(R.id.takeOffBtn);
        this.mRTLBtn = (Button) findViewById(R.id.rtlBtn);
        this.mLandBtn = (Button) findViewById(R.id.landBtn);
        this.mGoUpBtn = (Button) findViewById(R.id.goUp);
        this.mGoDownBtn = (Button) findViewById(R.id.goDown);
        this.mGoFWDBtn = (Button) findViewById(R.id.goFWD);
        this.mGoBackBtn = (Button) findViewById(R.id.goBack);
        this.mMissionBtn = (Button) findViewById(R.id.missionBtn);
        this.mErrorSpinner = (Spinner) findViewById(R.id.errorSpinner);
        this.initSpinner();
        this.mErrorID = -1;

        this.changeDroneStatus(eDroneStatus.NOT_CONNECTED);
        this.mDroneClient = new DroneClient(getApplicationContext());
        this.mDroneClient.execute();
    }

    private void initSpinner()
    {
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this, android.R.layout.simple_spinner_dropdown_item, getResources().getStringArray(R.array.errors));
        this.mErrorSpinner.setAdapter(adapter);
        this.mErrorSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener()
        {
            @Override
            public void onItemSelected(AdapterView<?> adapterView, View view, int i, long l)
            {
                mErrorID = i;
            }

            @Override
            public void onNothingSelected(AdapterView<?> adapterView)
            {
                mErrorID = -1;
            }
        });
    }

    private void create_logs()
    {
        File dir = new File(LOG_FOLDER);
        Boolean success = true;
        if (!dir.exists())
        {
            success = dir.mkdir();
        }
        if(success)
        {
            File proxy_log = new File(LOG_FOLDER + LOG_PROXY_NAME);
            File tracker_log = new File(LOG_FOLDER + LOG_TRACKER_NAME);
            FileOutputStream proxy_stream = null;
            FileOutputStream tracker_stream = null;
            try
            {
                proxy_stream = new FileOutputStream(proxy_log);
                tracker_stream = new FileOutputStream(tracker_log);
                for(int i = 0; i < 1000; ++i)
                {
                    proxy_stream.write(String.valueOf(i).getBytes());
                    tracker_stream.write(String.valueOf(1000 - i).getBytes());
                }
            }
            catch (Exception e){
                try
                {
                    proxy_stream.close();
                    tracker_stream.close();
                }
                catch (Exception e1)
                {
                    e1.printStackTrace();
                }
            }

        }
    }

    private void send_logs ()
    {
        File dir = new File(LOG_FOLDER);
        Boolean success = true;
        if (!dir.exists())
        {
            success = dir.mkdir();
        }
        if(success)
        {
            File[] files = dir.listFiles();
            for (File file : files)
            {
//                this.mDroneClient.sendFile(file);
            }
        }
    }

    public void changeDroneStatus(eDroneStatus status)
    {
        this.mDroneStatus = status;
        switch (this.mDroneStatus)
        {
            case NOT_CONNECTED:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.notConnected));
                this.mTakeOffBtn.setEnabled(true);
                this.mRTLBtn.setEnabled(false);
                this.mLandBtn.setEnabled(false);
                this.mGoUpBtn.setEnabled(false);
                this.mGoDownBtn.setEnabled(false);
                this.mGoFWDBtn.setEnabled(false);
                this.mGoBackBtn.setEnabled(false);
                this.mMissionBtn.setEnabled(false);
                break;
            }
            case ON_GROUND:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.onTheGround));
                this.mTakeOffBtn.setEnabled(true);
                this.mRTLBtn.setEnabled(false);
                this.mLandBtn.setEnabled(false);
                this.mGoUpBtn.setEnabled(false);
                this.mGoDownBtn.setEnabled(false);
                this.mGoFWDBtn.setEnabled(false);
                this.mGoBackBtn.setEnabled(false);
                this.mMissionBtn.setEnabled(false);
                this.create_logs();
                break;
            }
            case AIRBORNE:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.droneIsAirborne));
                this.mTakeOffBtn.setEnabled(false);
                this.mRTLBtn.setEnabled(true);
                this.mLandBtn.setEnabled(true);
                this.mGoUpBtn.setEnabled(true);
                this.mGoDownBtn.setEnabled(true);
                this.mGoFWDBtn.setEnabled(true);
                this.mGoBackBtn.setEnabled(true);
                this.mMissionBtn.setEnabled(true);
                ArrayMap<String, String> map = new ArrayMap<>();
                map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
                map.put("cmd", "airborn");
                map.put("is_error", String.valueOf(false));
                this.mDroneClient.sendMsg(map);
                break;
            }
            case LANDING:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.droneIsLanding));
                this.mTakeOffBtn.setEnabled(false);
                this.mRTLBtn.setEnabled(false);
                this.mLandBtn.setEnabled(false);
                this.mGoUpBtn.setEnabled(false);
                this.mGoDownBtn.setEnabled(false);
                this.mGoFWDBtn.setEnabled(false);
                this.mGoBackBtn.setEnabled(false);
                this.mMissionBtn.setEnabled(false);
                final Handler handler = new Handler();
                handler.postDelayed(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        mStatusLbl.setText(getResources().getString(R.string.landFin));
                        ArrayMap<String, String> map = new ArrayMap<>();
                        map.put("drone_num", String.valueOf(mDroneClient.getDroneNum()));
                        map.put("cmd", "landed");
                        map.put("is_error", String.valueOf(false));
                        mDroneClient.sendMsg(map);
//                        send_logs();
                    }
                }, shortDelay);
                break;
            }
            case ERROR:
            {
                this.mStatusLbl.setText(getResources().getString(R.string.droneIsLanding));
                this.mTakeOffBtn.setEnabled(false);
                this.mRTLBtn.setEnabled(false);
                this.mLandBtn.setEnabled(false);
                this.mGoUpBtn.setEnabled(false);
                this.mGoDownBtn.setEnabled(false);
                this.mGoFWDBtn.setEnabled(false);
                this.mGoBackBtn.setEnabled(false);
                this.mMissionBtn.setEnabled(false);
                final Handler handler = new Handler();
                handler.postDelayed(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        mStatusLbl.setText(getResources().getString(R.string.landFin));
                        ArrayMap<String, String> map = new ArrayMap<>();
                        map.put("drone_num", String.valueOf(mDroneClient.getDroneNum()));
                        map.put("cmd", "landed");
                        map.put("is_error", String.valueOf(true));
                        mDroneClient.sendMsg(map);
                    }
                }, shortDelay);
                break;
            }
        }
    }

    public void onClick_takeOff(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        this.mStatusLbl.setText(getResources().getString(R.string.takeOfflbl));
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "takeoff");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable()
        {
            @Override
            public void run()
            {
                changeDroneStatus(eDroneStatus.AIRBORNE);
            }
        }, shortDelay);

    }

    public void onClick_rtl(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "rtl");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        changeDroneStatus(eDroneStatus.LANDING);
    }

    public void onClick_land(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "land");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        changeDroneStatus(eDroneStatus.LANDING);
    }

    public void onClick_up(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "ascending");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        this.mStatusLbl.setText(getResources().getString(R.string.goUp));
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable()
        {
            @Override
            public void run()
            {
                changeDroneStatus(eDroneStatus.AIRBORNE);

            }
        }, shortDelay);
    }

    public void onClick_down(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "descending");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        this.mStatusLbl.setText(getResources().getString(R.string.goDown));
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable()
        {
            @Override
            public void run()
            {
                changeDroneStatus(eDroneStatus.AIRBORNE);

            }
        }, shortDelay);
    }

    public void onClick_fwd(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "going_fwd");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        this.mStatusLbl.setText(getResources().getString(R.string.goFWD));
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable()
        {
            @Override
            public void run()
            {
                changeDroneStatus(eDroneStatus.AIRBORNE);

            }
        }, shortDelay);
    }

    public void onClick_back(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "go_back");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        this.mStatusLbl.setText(getResources().getString(R.string.goBack));
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable()
        {
            @Override
            public void run()
            {
                changeDroneStatus(eDroneStatus.AIRBORNE);

            }
        }, shortDelay);
    }

    public void onClick_mission(View view)
    {
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", "in_mission");
        map.put("is_error", String.valueOf(false));
        this.mDroneClient.sendMsg(map);
        this.mStatusLbl.setText(getResources().getString(R.string.inMission));
        final Handler handler = new Handler();
        handler.postDelayed(new Runnable()
        {
            @Override
            public void run()
            {
                changeDroneStatus(eDroneStatus.AIRBORNE);

            }
        }, longDelay);
    }

    public void onClick_subServerIP(View view)
    {
        Config.serverIP = this.mServerIpEntry.getText().toString();
        this.mDroneClient.closeConnection();
        this.mDroneClient = new DroneClient(getApplicationContext());
        this.mDroneClient.execute();
        Toast.makeText(this, "server ip changed", Toast.LENGTH_SHORT).show();
    }

    public void onClick_sendError(View view)
    {
        if(this.mDroneStatus != eDroneStatus.AIRBORNE || this.mErrorID == -1)
        {
            return;
        }
        String[] array = getResources().getStringArray(R.array.errors);
        ArrayMap<String, String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneClient.getDroneNum()));
        map.put("cmd", array[mErrorID]);
        map.put("is_error", String.valueOf(true));
        this.mDroneClient.sendMsg(map);
        this.changeDroneStatus(eDroneStatus.ERROR);
        if(mErrorID == 0)
        {
            this.mStatusLbl.setText(getResources().getString(R.string.droneCrash));
        }
    }

    public static MainActivity getInstance()
    {
        return instance;
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
