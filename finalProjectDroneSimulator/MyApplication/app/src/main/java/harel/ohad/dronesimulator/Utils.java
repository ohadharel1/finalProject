package harel.ohad.dronesimulator;

import android.util.ArrayMap;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

/**
 * Created by ohad on 05-Mar-17.
 */

public class Utils
{
//    public static JSONArray stringToJson(String jsonString)
//    {
//
//    }
//
//    public static String jsonToString(JSONArray jsonArray)
//    {
//
//    }

    public static String mapToJsonString(Map<String, String> jsonMap)
    {
        try
        {
            JSONArray jsonArray = new JSONArray("[" + jsonMap.toString() + "]");
            return jsonArray.toString();
        }
        catch (JSONException e)
        {
            e.printStackTrace();
            return null;
        }
    }

    public static Map<String, String> jsonStringToMap(String jsonString)
    {
        ArrayMap<String, String> jsonMap = new ArrayMap<String, String>();
        try
        {
            JSONObject jsonObject = new JSONObject(jsonString);
            String key = null;
            String value = null;
            Iterator<String> keysItr = jsonObject.keys();
            while (keysItr.hasNext())
            {
                key = keysItr.next();
                value = jsonObject.getString(key);
                jsonMap.put(key, value);
            }
        }
        catch (JSONException e)
        {
            e.printStackTrace();
        }

        return jsonMap;
    }
}
