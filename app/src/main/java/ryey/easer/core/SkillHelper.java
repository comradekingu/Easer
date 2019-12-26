/*
 * Copyright (c) 2016 - 2019 Rui Zhao <renyuneyun@gmail.com>
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

package ryey.easer.core;

import android.content.Context;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import java.util.UUID;

import ryey.easer.commons.local_skill.dynamics.SolidDynamicsAssignment;
import ryey.easer.commons.local_skill.operationskill.Loader;
import ryey.easer.commons.local_skill.operationskill.OperationData;
import ryey.easer.commons.local_skill.operationskill.OperationSkill;
import ryey.easer.core.data.RemoteLocalOperationDataWrapper;
import ryey.easer.remote_plugin.RemoteOperationData;
import ryey.easer.skills.LocalSkillRegistry;

/**
 * A helper class which combines local and remote skills, and exposes interfaces as if there is no difference.
 *
 * Async is needed. This class uses {@link AsyncHelper} and {@link RemotePluginCommunicationHelper}
 *
 * A lot todo: more types & include UI
 */
public final class SkillHelper {

    private SkillHelper() {}

    public static class OperationHelper {

        private final Context context;
        private final RemotePluginCommunicationHelper helper;
        private final LocalSkillRegistry.Registry<OperationSkill, OperationData> operationRegistry = LocalSkillRegistry.getInstance().operation();

        public OperationHelper(Context context) {
            this.context = context;
            this.helper = new RemotePluginCommunicationHelper(context);
        }

        public void begin() {
            helper.begin();
        }

        public void end() {
            helper.end();
        }

        /**
         *
         * @param jobId
         * @param skillId
         * @param data
         * @param solidDynamicsAssignment
         * @param callback
         * @return succeeded to run the job or not
         */
        public boolean triggerOperation(UUID jobId, String skillId, RemoteLocalOperationDataWrapper data, SolidDynamicsAssignment solidDynamicsAssignment, OnOperationLoadResultCallback callback) {
            if (operationRegistry.hasSkill(skillId)) {
                OperationSkill plugin = operationRegistry.findSkill(skillId);
                assert plugin != null;
                Loader loader = plugin.loader(context);
                OperationData localData = data.localData;
                assert localData != null;
                //noinspection unchecked
                loader.load(localData.applyDynamics(solidDynamicsAssignment), (success -> {
                    callback.onResult(jobId, success); // TODO: Remove this second-layer callback
                }));
            } else {
                RemoteOperationData remoteData = data.remoteData;
                helper.asyncTriggerOperation(jobId, skillId, remoteData, callback);
            }
            return true;
        }

//        public int triggerOperations(String skillId, Collection<RemoteLocalOperationDataWrapper> dataCollection, SolidDynamicsAssignment solidMacroAssignment, OnOperationLoadResultCallback callback) {
//            int count = 0;
//            if (operationRegistry.hasSkill(skillId)) {
//                OperationSkill plugin = operationRegistry.findSkill(skillId);
//                assert plugin != null;
//                Loader loader = plugin.loader(context);
//                for (RemoteLocalOperationDataWrapper data : dataCollection) {
//                    count++;
//                    OperationData localData = data.localData;
//                    assert localData != null;
//                    //noinspection unchecked
//                    loader.load(localData.applyDynamics(solidMacroAssignment), (success -> {
//                        callback.onResult(skillId, success); // TODO: Remove this second-layer callback
//                    }));
//                }
//            } else {
//                for (RemoteLocalOperationDataWrapper data : dataCollection) {
//                    count++;
//                    RemoteOperationData remoteData = data.remoteData;
//                    helper.asyncTriggerOperation(skillId, remoteData); //TODO: listen remote result
//                    callback.onResult(skillId, true);
//                }
//            }
//            return count;
//        }

        public interface OnOperationLoadResultCallback {
            void onResult(@NonNull UUID id, @Nullable Boolean success);
        }

    }

}
