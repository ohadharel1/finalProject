package harel.ohad.dronesimulator;

import android.content.Context;
import android.net.wifi.WifiManager;
import android.os.AsyncTask;
import android.text.format.Formatter;
import android.util.ArrayMap;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
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
    private Context mContext;

    public DroneClient(Context context)
    {
        mMessage = null;
        this.mDroneNum = findDroneNum(context);
        this.mConnectionAlive = true;
        this.mContext = context;
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

        DatagramSocket socket = null;
        try
        {
            String ip = Config.serverIP;
            int port = Config.serverPort;
//            socket.connect(new InetSocketAddress(ip, port));
            MainActivity.getInstance().runOnUiThread(new Runnable()
            {
                @Override
                public void run()
                {
                    MainActivity.getInstance().changeDroneStatus(MainActivity.eDroneStatus.ON_GROUND);
                }
            });
            while (this.mConnectionAlive)
            {
                if (mMessage != null)
                {
                    socket = new DatagramSocket();
                    int length = mMessage.length();
                    byte [] msg = mMessage.getBytes();
                    InetAddress addr = InetAddress.getByName("10.0.0.6");
                    DatagramPacket p = new DatagramPacket(msg, length, addr, 10001);
//                    Toast.makeText(this.mContext, "SENDING MSG", Toast.LENGTH_LONG).show();
                    System.out.println("*****SENDING MSG******");
                    System.out.println(ip + port + mMessage + length);
                    socket.send(p);
                    System.out.println(p);
                    mMessage = null;
                }
            }
            System.err.println("*****OUT OF WHILE******");
//            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream(1024);
//            byte[] buffer = new byte[1024];
        }
        catch (Exception e)
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
                catch (Exception e)
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
