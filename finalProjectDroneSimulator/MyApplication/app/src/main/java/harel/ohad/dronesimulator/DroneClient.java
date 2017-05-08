package harel.ohad.dronesimulator;

import android.content.Context;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.text.format.Formatter;
import android.util.ArrayMap;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.NetworkInterface;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Enumeration;
import java.util.Map;

import static android.content.Context.WIFI_SERVICE;

/**
 * Created by ohad on 04-Mar-17.
 */

public class DroneClient extends AsyncTask<Void, Void, Void>
{
    private int mDroneNum;
    private static String mMessage;
    private boolean mConnectionAlive;

    public DroneClient(Context context)
    {
        mMessage = null;
        this.mDroneNum = findDroneNum(context);
        this.mConnectionAlive = true;
    }

    private int findDroneNum(final Context context)
    {
        String ipAddr = null;
        try
        {
            WifiManager wm = (WifiManager) context.getSystemService(WIFI_SERVICE);
            ipAddr = Formatter.formatIpAddress(wm.getConnectionInfo().getIpAddress());
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        String bytes[] = ipAddr.split("\\.");
        return Integer.valueOf(bytes[3]);
    }

    public int getDroneNum()
    {
        return this.mDroneNum;
    }

    @Override
    protected Void doInBackground(Void... voids)
    {

        Socket socket = null;
        try
        {
            String ip = Config.serverIP;
            int port = Config.serverPort;
            socket = new Socket();
            socket.connect(new InetSocketAddress(ip, port), 1000);
            MainActivity.getInstance().runOnUiThread(new Runnable()
            {
                @Override
                public void run()
                {
                    MainActivity.getInstance().changeDroneStatus(MainActivity.eDroneStatus.ON_GROUND);
                }
            });
            OutputStream out = socket.getOutputStream();
            while (this.mConnectionAlive)
            {
                if (mMessage != null)
                {
                    out.write(mMessage.getBytes());
                    mMessage = null;
                }
            }
//            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(1024);
//            byte[] buffer = new byte[1024];
        }
        catch (IOException e)
        {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        finally
        {
            if (socket != null)
            {
                try
                {
                    socket.close();
                }
                catch (IOException e)
                {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }
        return null;
    }

    public void sendMsg(String msg)
    {
        mMessage = msg;
    }

    public void sendMsg(Map<String, String> msg)
    {
        mMessage = Utils.mapToJsonString(msg);
    }

    public void closeConnection()
    {
        ArrayMap<String,String> map = new ArrayMap<>();
        map.put("drone_num", String.valueOf(this.mDroneNum));
        map.put("cmd", "fin");
        mMessage = Utils.mapToJsonString(map);
        this.mConnectionAlive = false;
    }


}
