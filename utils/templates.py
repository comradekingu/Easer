#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
#   Author  :   renyuneyun
#   E-mail  :   renyuneyun@gmail.com
#   Date    :   18/04/22 01:00:10
#   License :   Apache 2.0 (See LICENSE)
#

'''

'''

tmpl_copyright = '''/*
 * Copyright (c) 2016 - 2018 Rui Zhao <renyuneyun@gmail.com>
 *
 * This file is part of Easer.
 *
 * Easer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Easer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Easer.  If not, see <http://www.gnu.org/licenses/>.
 */
'''

tmpl_skill_view_fragment = '''package {package};

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import ryey.easer.commons.local_skill.InvalidDataInputException;
import ryey.easer.skills.SkillViewFragment;
import ryey.easer.commons.local_skill.ValidData;

public class {view_fragment} extends SkillViewFragment<{data}> {{

    @NonNull
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {{
        //TODO
    }}

    @Override
    protected void _fill(@ValidData @NonNull {data} data) {{
        //TODO
    }}

    @ValidData
    @NonNull
    @Override
    public {data} getData() throws InvalidDataInputException {{
        //TODO
    }}
}}
'''

tmpl_androidTest_data = '''package {package};

import android.os.Parcel;

import org.junit.Test;

import ryey.easer.skills.TestHelper;

import static org.junit.Assert.assertEquals;

public class {androidTest$data} {{

    @Test
    public void testParcel() {{
        {data} dummyData = new {data_factory}().dummyData();
        Parcel parcel = TestHelper.writeToParcel(dummyData);
        {data} parceledData = {data}.CREATOR.createFromParcel(parcel);
        assertEquals(dummyData, parceledData);
    }}

}}
'''

tmpl_operation_skill = '''package {package};

import android.app.Activity;
import android.content.Context;

import androidx.annotation.NonNull;

import ryey.easer.skills.SkillViewFragment;
import ryey.easer.commons.local_skill.operationskill.OperationDataFactory;
import ryey.easer.skills.operation.OperationLoader;
import ryey.easer.commons.local_skill.operationskill.OperationSkill;
import ryey.easer.commons.local_skill.operationskill.PrivilegeUsage;

public class {skill} implements OperationSkill<{data}> {{

    @NonNull
    @Override
    public String id() {{
        return "{id}";
    }}

    @Override
    public int name() {{
        //TODO
    }}

    @Override
    public boolean isCompatible(@NonNull final Context context) {{
        return true;
    }}

    @NonNull
    @Override
    public PrivilegeUsage privilege() {{
        return PrivilegeUsage.no_root;
    }}

    @Override
    public int maxExistence() {{
        return 0;
    }}

    @Override
    public boolean checkPermissions(@NonNull Context context) {{
        return true;
    }}

    @Override
    public void requestPermissions(@NonNull Activity activity, int requestCode) {{
    }}

    @NonNull
    @Override
    public OperationDataFactory<{data}> dataFactory() {{
        return new {data_factory}();

    }}

    @NonNull
    @Override
    public SkillViewFragment<{data}> view() {{
        return new {view_fragment}();
    }}

    @NonNull
    @Override
    public OperationLoader<{data}> loader(@NonNull Context context) {{
        return new {loader}(context);
    }}

}}
'''

tmpl_operation_data_factory = '''package {package};

import androidx.annotation.NonNull;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.commons.local_skill.operationskill.OperationDataFactory;
import ryey.easer.plugin.PluginDataFormat;

class {data_factory} implements OperationDataFactory<{data}> {{
    @NonNull
    @Override
    public Class<{data}> dataClass() {{
        return {data}.class;
    }}

    @ValidData
    @NonNull
    @Override
    public {data} dummyData() {{
        //TODO
    }}

    @ValidData
    @NonNull
    @Override
    public {data} parse(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        return new {data}(data, format, version);
    }}
}}
'''

tmpl_operation_data = '''package {package};

import android.os.Parcel;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.Set;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.dynamics.SolidDynamicsAssignment;
import ryey.easer.commons.local_skill.operationskill.OperationData;
import ryey.easer.plugin.PluginDataFormat;

public class {data} implements OperationData {{
    {data}(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        //TODO
    }}

    @NonNull
    @Override
    public String serialize(@NonNull PluginDataFormat format) {{
        //TODO
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean isValid() {{
        //TODO
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean equals(Object obj) {{
        if (obj == this)
            return true;
        if (obj == null || !(obj instanceof {data}))
            return false;
        //TODO
        return true;
    }}

    @Nullable
    @Override
    public Set<String> placeholders() {{
        return null;
    }}

    @NonNull
    @Override
    public OperationData applyDynamics(SolidDynamicsAssignment dynamicsAssignment) {{
        return this;
    }}

    @Override
    public int describeContents() {{
        return 0;
    }}

    @Override
    public void writeToParcel(Parcel dest, int flags) {{
        //TODO
    }}

    public static final Creator<{data}> CREATOR
            = new Creator<{data}>() {{
        public {data} createFromParcel(Parcel in) {{
            return new {data}(in);
        }}

        public {data}[] newArray(int size) {{
            return new {data}[size];
        }}
    }};

    private {data}(Parcel in) {{
        //TODO
    }}
}}
'''

tmpl_operation_loader = '''package {package};

import android.content.Context;

import androidx.annotation.NonNull;

import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.skills.operation.OperationLoader;

public class {loader} extends OperationLoader<{data}> {{
    {loader}(Context context) {{
        super(context);
    }}

    @Override
    public boolean load(@ValidData @NonNull {data} data) {{
        //TODO
    }}
}}
'''

tmpl_event_skill = '''package {package};

import android.app.Activity;
import android.content.Context;

import androidx.annotation.NonNull;

import ryey.easer.R;
import ryey.easer.skills.SkillViewFragment;
import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.skills.event.AbstractSlot;
import ryey.easer.commons.local_skill.eventskill.EventDataFactory;
import ryey.easer.commons.local_skill.eventskill.EventSkill;

public class {skill} implements EventSkill<{data}> {{

    @NonNull
    @Override
    public String id() {{
        return "{id}";
    }}

    @Override
    public int name() {{
        //TODO
    }}

    @Override
    public boolean isCompatible(@NonNull final Context context) {{
        return true;
    }}

    @Override
    public boolean checkPermissions(@NonNull Context context) {{
        return true;
    }}

    @Override
    public void requestPermissions(@NonNull Activity activity, int requestCode) {{
    }}

    @NonNull
    @Override
    public EventDataFactory<{data}> dataFactory() {{
        return new {data_factory}();
    }}

    @NonNull
    @Override
    public SkillViewFragment<{data}> view() {{
        return new {view_fragment}();
    }}

    @Override
    public AbstractSlot<{data}> slot(@NonNull Context context, @ValidData @NonNull {data} data) {{
        return new {slot}(context, data);
    }}

    @Override
    public AbstractSlot<{data}> slot(@NonNull Context context, @NonNull {data} data, boolean retriggerable, boolean persistent) {{
        return new {slot}(context, data, retriggerable, persistent);
    }}

}}
'''

tmpl_event_data_factory = '''package {package};

import androidx.annotation.NonNull;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.commons.local_skill.eventskill.EventDataFactory;
import ryey.easer.plugin.PluginDataFormat;

class {data_factory} implements EventDataFactory<{data}> {{
    @NonNull
    @Override
    public Class<{data}> dataClass() {{
        return {data}.class;
    }}

    @ValidData
    @NonNull
    @Override
    public {data} dummyData() {{
        //TODO
    }}

    @ValidData
    @NonNull
    @Override
    public {data} parse(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        return new {data}(data, format, version);
    }}
}}
'''

tmpl_event_data = '''package {package};

import android.os.Parcel;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.dynamics.Dynamics;
import ryey.easer.skills.event.AbstractEventData;
import ryey.easer.plugin.PluginDataFormat;

public class {data} extends AbstractEventData {{

    {data}(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        //TODO
    }}

    @NonNull
    @Override
    public String serialize(@NonNull PluginDataFormat format) {{
        String res;
        //TODO
        return res;
    }}

    @Nullable
    @Override
    public Dynamics[] dynamics() {{
        return null;
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean isValid() {{
        //TODO
        return true;
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean equals(Object obj) {{
        if (obj == null || !(obj instanceof {data}))
            return false;
        //TODO
        return true;
    }}

    @Override
    public int describeContents() {{
        return 0;
    }}

    @Override
    public void writeToParcel(Parcel dest, int flags) {{
        //TODO
    }}

    public static final Creator<{data}> CREATOR
            = new Creator<{data}>() {{
        public {data} createFromParcel(Parcel in) {{
            return new {data}(in);
        }}

        public {data}[] newArray(int size) {{
            return new {data}[size];
        }}
    }};

    private {data}(Parcel in) {{
        //TODO
    }}
}}
'''

tmpl_event_slot = '''package {package};

import android.content.Context;

import ryey.easer.skills.event.AbstractSlot;

public class {slot} extends AbstractSlot<{data}> {{

    {slot}(Context context, {data} data) {{
        this(context, data, RETRIGGERABLE_DEFAULT, PERSISTENT_DEFAULT);
    }}

    {slot}(Context context, {data} data, boolean retriggerable, boolean persistent) {{
        super(context, data, retriggerable, persistent);
    }}

    @Override
    public void listen() {{
        //TODO
    }}

    @Override
    public void cancel() {{
        //TODO
    }}

}}
'''

tmpl_condition_skill = '''package {package};

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Context;

import androidx.annotation.NonNull;

import ryey.easer.skills.SkillViewFragment;
import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.commons.local_skill.conditionskill.ConditionDataFactory;
import ryey.easer.commons.local_skill.conditionskill.ConditionSkill;
import ryey.easer.commons.local_skill.conditionskill.Tracker;

public class {skill} implements ConditionSkill<{data}> {{

    @NonNull
    @Override
    public String id() {{
        return "{id}";
    }}

    @Override
    public int name() {{
        //TODO
    }}

    @Override
    public boolean isCompatible(@NonNull final Context context) {{
        return true;
    }}

    @Override
    public boolean checkPermissions(@NonNull Context context) {{
        return true;
    }}

    @Override
    public void requestPermissions(@NonNull Activity activity, int requestCode) {{
    }}

    @NonNull
    @Override
    public ConditionDataFactory<{data}> dataFactory() {{
        return new {data_factory}();
    }}

    @NonNull
    @Override
    public SkillViewFragment<{data}> view() {{
        return new {view_fragment}();
    }}

    @NonNull
    @Override
    public Tracker<{data}> tracker(@NonNull Context context,
                                                 @ValidData @NonNull {data} data,
                                                 @NonNull PendingIntent event_positive,
                                                 @NonNull PendingIntent event_negative) {{
        return new {tracker}(context, data, event_positive, event_negative);
    }}

}}
'''

tmpl_condition_data_factory = '''package {package};

import androidx.annotation.NonNull;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.commons.local_skill.conditionskill.ConditionDataFactory;
import ryey.easer.plugin.PluginDataFormat;

class {data_factory} implements ConditionDataFactory<{data}> {{
    @NonNull
    @Override
    public Class<{data}> dataClass() {{
        return {data}.class;
    }}

    @ValidData
    @NonNull
    @Override
    public {data} dummyData() {{
        //TODO
    }}

    @ValidData
    @NonNull
    @Override
    public {data} parse(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        return new {data}(data, format, version);
    }}
}}
'''

tmpl_condition_data = '''package {package};

import android.os.Parcel;

import androidx.annotation.NonNull;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.conditionskill.ConditionData;
import ryey.easer.plugin.PluginDataFormat;

public class {data} implements ConditionData {{

    {data}(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        switch (format) {{
            default:
                //TODO
        }}
    }}

    @NonNull
    @Override
    public String serialize(@NonNull PluginDataFormat format) {{
        String res;
        switch (format) {{
            default:
                //TODO
        }}
        return res;
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean isValid() {{
        //TODO
        return false;
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean equals(Object obj) {{
        if (obj == this)
            return true;
        if (obj == null || !(obj instanceof {data}))
            return false;
        //TODO
        return true;
    }}

    @Override
    public int describeContents() {{
        return 0;
    }}

    @Override
    public void writeToParcel(Parcel dest, int flags) {{
        //TODO
    }}

    public static final Creator<{data}> CREATOR
            = new Creator<{data}>() {{
        public {data} createFromParcel(Parcel in) {{
            return new {data}(in);
        }}

        public {data}[] newArray(int size) {{
            return new {data}[size];
        }}
    }};

    private {data}(Parcel in) {{
        //TODO
    }}
}}
'''

tmpl_condition_tracker = '''package {package};

import android.app.PendingIntent;
import android.content.Context;

import androidx.annotation.NonNull;

import ryey.easer.skills.condition.SkeletonTracker;

public class {tracker} extends SkeletonTracker<{data}> {{

    {tracker}(Context context, {data} data,
                   @NonNull PendingIntent event_positive,
                   @NonNull PendingIntent event_negative) {{
        super(context, data, event_positive, event_negative);
    }}

    @Override
    public void start() {{
        //TODO
    }}

    @Override
    public void stop() {{
        //TODO
    }}

    @Override
    public Boolean state() {{
        //TODO
    }}
}}
'''

tmpl_usource_slot = tmpl_event_slot
tmpl_usource_tracker = tmpl_condition_tracker

tmpl_usource_skill = '''package {package};

import android.app.Activity;
import android.app.PendingIntent;
import android.content.Context;

import androidx.annotation.NonNull;

import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.commons.local_skill.conditionskill.Tracker;
import ryey.easer.commons.local_skill.eventskill.Slot;
import ryey.easer.commons.local_skill.usource.USourceDataFactory;
import ryey.easer.commons.local_skill.usource.USourceSkill;
import ryey.easer.skills.SkillViewFragment;

public class {skill} implements USourceSkill<{data}> {{

    @NonNull
    @Override
    public String id() {{
        return "{id}";
    }}

    @Override
    public int name() {{
        //TODO
    }}

    @Override
    public boolean isCompatible(@NonNull final Context context) {{
        //TODO
    }}

    @Override
    public Boolean checkPermissions(@NonNull Context context) {{
        //TODO
    }}

    @Override
    public void requestPermissions(@NonNull Activity activity, int requestCode) {{
    }}

    @NonNull
    @Override
    public USourceDataFactory<{data}> dataFactory() {{
        return new {data_factory}();
    }}

    @NonNull
    @Override
    public SkillViewFragment<{data}> view() {{
        return new {view_fragment}();
    }}

    @Override
    public Slot<{data}> slot(@NonNull Context context, @NonNull {data} data) {{
        return new {slot}(context, data);
    }}

    @Override
    public Slot<{data}> slot(@NonNull Context context, @NonNull {data} data, boolean retriggerable, boolean persistent) {{
        return new {slot}(context, data, retriggerable, persistent);
    }}

    @NonNull
    @Override
    public Tracker<{data}> tracker(@NonNull Context context,
                                            @ValidData @NonNull {data} data,
                                            @NonNull PendingIntent event_positive,
                                            @NonNull PendingIntent event_negative) {{
        return new {tracker}(context, data, event_positive, event_negative);
    }}

}}
'''

tmpl_usource_data = '''package {package};

import android.os.Parcel;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.dynamics.Dynamics;
import ryey.easer.commons.local_skill.usource.USourceData;
import ryey.easer.plugin.PluginDataFormat;

public class {data} implements USourceData {{

    {data}(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        switch (format) {{
            default:
                //TODO
        }}
    }}

    @NonNull
    @Override
    public String serialize(@NonNull PluginDataFormat format) {{
        String res;
        switch (format) {{
            default:
                //TODO
        }}
        return res;
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean isValid() {{
        //TODO
        return false;
    }}

    @Nullable
    @Override
    public Dynamics[] dynamics() {{
        return null;
    }}

    @SuppressWarnings({{"SimplifiableIfStatement", "RedundantIfStatement"}})
    @Override
    public boolean equals(Object obj) {{
        if (obj == this)
            return true;
        if (obj == null || !(obj instanceof {data}))
            return false;
        //TODO
        return true;
    }}

    @Override
    public int describeContents() {{
        return 0;
    }}

    @Override
    public void writeToParcel(Parcel dest, int flags) {{
        //TODO
    }}

    public static final Creator<{data}> CREATOR
            = new Creator<{data}>() {{
        public {data} createFromParcel(Parcel in) {{
            return new {data}(in);
        }}

        public {data}[] newArray(int size) {{
            return new {data}[size];
        }}
    }};

    private {data}(Parcel in) {{
        //TODO
    }}
}}
'''

tmpl_usource_data_factory = '''package {package};

import androidx.annotation.NonNull;

import ryey.easer.commons.local_skill.IllegalStorageDataException;
import ryey.easer.commons.local_skill.ValidData;
import ryey.easer.commons.local_skill.usource.USourceDataFactory;
import ryey.easer.plugin.PluginDataFormat;

class {data_factory} implements USourceDataFactory<{data}> {{
    @NonNull
    @Override
    public Class<{data}> dataClass() {{
        return {data}.class;
    }}

    @ValidData
    @NonNull
    @Override
    public {data} dummyData() {{
        //TODO
    }}

    @ValidData
    @NonNull
    @Override
    public {data} parse(@NonNull String data, @NonNull PluginDataFormat format, int version) throws IllegalStorageDataException {{
        return new {data}(data, format, version);
    }}
}}
'''

